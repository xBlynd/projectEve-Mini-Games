# import only system from os 
import os

# used for the random attacks.  Need to implement to heal.
from random import randint
import time
import json

# this turns the game persistant.  
game_running = True
# stat manager
game_results = []

# this will be used to calculate the random attack from the warriors.
def calculate_warrior_attack(attack_min, attack_max):
    return randint(attack_min, attack_max)

def calculate_player_heal(heal_min, heal_max):
    return randint(heal_min, heal_max)

# Winner annoucement Function
def game_ends(winner_name):
    print(f'{winner_name} won the game')
    print('projectEve is made with ', u"\u2661")

# Loads the local storage into memory
def loadLocalStorage():
    localStorageFilename = 'localstorage.json'
    try:
        with open(localStorageFilename, 'r') as infile:
            return json.load(infile)
    except Exception as e:
        print(f'Error loading: {e}')
        return None

# Saves the local storage back into memory
# Do your code here pliz
def saveLocalStorage(obj):
    saveStorageFilename = 'localstorage.json'
    try:
        # Save here
        with open(saveStorageFilename, 'w') as outfile:
            json.dump(obj, outfile, indent=4)

    except Exception as e:
        print(f'Failed to save file: {e}')

# this keeps the game running while the code below continues
while game_running:

    #counter.  Counts the rounds .
    counter = 0
    # at the end of the game this starts a new round.  1st Round Loop
    new_round = True
    #disctionary

    # Load data and make sure it exists
    # gameData = loadLocalStorage()    //this line has been removed until storage is functioning correctly
    # There has to be a better way to categorize these.  
    # Levels or masterclass of some sorts needs to be added.  Not quite sure how to achive this take.  Maybe a multiplier to all traits above the class tier???
    gameData = loadLocalStorage()
    if 'player' not in gameData:
        gameData['player'] = {
            'name': '',
            'attack': 13,
            'heal': 16,
            'heal_min': 14,
            'heal_max': 20,
            'health': 100,
            'stamina': 10,
            'armor': 11
        }

# Need to add randomize on race encounter.  However when a map is built we will move it to area placements.
    if 'warrior' not in gameData:
        gameData['warrior'] = {
            'name': 'warrior',
            'race': ['human', 'barbarian', 'orc', 'troll', 'elf', 'woodelf', 'nightelf', 'dwarf'],
            'attack_min': 10,
            'attack_max': 20,
            'health': 100,
            'stamina': 10,
            'armor': 11
        }

#Will have to eventually seperate animals by type as some are stronger then others.  Need to research the best way to create this as to save time..
    if 'animals' not in gameData:
        gameData['animals'] = {
            'type': '',
            'health_min': 55,
            'health_max': 100,
            'stamina_min': 60,
            'stamina_max': 100,
            'attack_min': 3,
            'attack_max': 20
        }
    #added to help with the error on function before variable.  IDK why this works....
    # print(calculate_warrior_attack(gameData['warrior']['attack_min'], gameData['warrior']['attack_max']))


    # Player name input.  Should find a way to add this before the game starts.  Follow suit with stats page

    print('projectEvolved Boss Battle!')
    print('---' * 8)
    gameData['player']['name'] = input('Enter Name: ')

    print(f'{gameData["player"]["name"]} has {gameData["player"]["health"]} health')
    print(f'{gameData["warrior"]["name"]} has {gameData["warrior"]["health"]} health')

    # keeps the game running while the conditions below are running.  Second (y) round loop
    while new_round:
        
        #counter adds +1 per round.
        counter = counter + 1
        player_won = False
        warrior_won = False

        #prints input options.  Has to be a better way to do this.
        print('---' * 8)
        print('Please select action')
        print('---' * 8)
        print('1) Attack')
        print('2) Heal')
        print('3) Exit Game')
        print('4) Show Results')
        print('---' * 8)


        # input method from options above
        player_choice = input()


        #attack this warrior
        if player_choice == '1':
            gameData['warrior']['health'] -= gameData['player']['attack']
            if gameData['warrior']['health'] <= 0:
                player_won = True
            else:
                gameData['player']['health'] -= calculate_warrior_attack(gameData['warrior']['attack_min'], gameData['warrior']['attack_max'])
                if gameData['player']['health'] <= 0:
                    warrior_won = True


        # the elif is if player input picks option 2.  This initates the heal.
        elif player_choice == '2':
            player_heal = randint(gameData['player']['heal_min'], gameData['player']['heal_max'])
            gameData['player']['health'] +=calculate_player_heal(gameData['player']['heal_min'], gameData['player']['heal_max'])

            # Radommize added to attack
            warrior_attack = randint(gameData['warrior']['attack_min'], gameData['warrior']['attack_max'])
            gameData['player']['health'] -= calculate_warrior_attack(gameData['warrior']['attack_min'], gameData['warrior']['attack_max'])
            if gameData['player']['health'] <= 0:
                warrior_won = True

        elif player_choice == '3':
            new_round = False
            game_running = False
            print('---' * 8)
            print('See you soon dick.. Bye!')

        # Input option 4 to print the previous game results.  Need to put this before the game starts.  Should be able to see before join game
        elif player_choice == '4':
            for player_stats in game_results:
                print(player_stats)
        
        # if the user inputs a invalid options.  This will return a message
        else:
            print('not a option try again.')

        if (not player_won) and (not warrior_won):
            os.system('cls')
            print('###' * 8)
            print(f'{gameData["player"]["name"]} has {gameData["player"]["health"]} left')
            print(f'{gameData["warrior"]["name"]} has {gameData["warrior"]["health"]} left')
            print('###' * 8)
        

        #functions for the winner announements from above.  Game ending conditions
        elif player_won:
            os.system('cls')
            game_ends(gameData['player']['name'])
            # captures the game results for stat board
            round_result = {'name': gameData['player']['name'], 'health': gameData['player']['health'],'round': counter}
            game_results.append(round_result)
            time.sleep(5)
            new_round = False

        elif warrior_won:
            os.system('cls')
            game_ends(gameData['warrior']['name'])
            # captures the game results for stat board
            round_result = {'name': gameData['warrior']['name'], 'health': gameData['warrior']['health'], 'round': counter}
            game_results.append(round_result)
            time.sleep(5)
            new_round = False

         #New Round function from above
        if player_won == True or warrior_won == True:
            new_round = False


d