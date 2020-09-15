import os
import time

os.system('clear')
print("Welcome to the \"Logic Episodes\"!")

name = input("Enter your name: ")
age = int(input("Enter your age: "))
health = 10
game_over = False
chance = 0
stage = 0

def the_end():
    global game_over, chance
    game_over = True
    chance += 1
    print('Player', name,'used' , chance, 'chances and went through', stage, 'stages')
    time.sleep(2)
    return game_over

def show_health():
        print('Now, your health is', health,'.')
        
def check_health():
    global health, game_over
    if health == 0:
        print("Sorry, your health reached 0, so you lost the game, unfortunately...")
        game_over = the_end()
        
def train():
    print("You successfully entered the train. To be continued...")
    print('You finished the game with', health,'health points...')
    global stage, game_over
    stage +=1
    time.sleep(3)
    #c = input('Press Enter to repeat or write \"exit\" to leave the game...')
    #if c == 'exit':
    game_over = the_end()
    
def railway():
    print('\nOn the right you`ve noticed girl attached to the rails with rods...')
    print('\nAt the same time, you`ve been yelled at to enter the train because the boarding is going to end in a minute.')
    print('\"I feel exhausted already, but I have no ticket nor money... What should I do?\" ')
    ans2 = input('\nWould you choose to try to save the girl and stay in woods or get on the train and save yourself? (girl/train) ').lower()
    global stage, chance, game_over
    stage +=1
    if ans2 == 'health':
        show_health()
        ans2 = input('Enter the answer here: ').lower()
    if ans2 == 'girl':
        print('You didn`t manage to untie the girl till the train started moving.\n As you could no longer leave her alone, because she was beautiful as rose, you continued the saving procedure and \nyou both were hit by the train which you could be in')
        game_over = the_end()
    elif ans2 == 'train':
        print('You decided to get into the train...')
        train()
    else:
        print('You entered an unknown word, so you lost...')
        chance += 1
        time.sleep(2)
        game_over = the_end()

def game():
    global health, chance, stage, game_over
    while game_over != True:
        stage = 0
        os.system('clear')
        print("It`s late evening in the woods. And you`re totally lost.")
        print('\n\"Who knew that an ordinary walk through the forest could take so looong.\nWhere should I go now?')
        print('It`s already so dark, I cannot see further than 2 metres ahead...\nI have got sore throat while tried to seek for help...\"')
        print('\nYou hear some chattering on the left, but cannot hear the words, it could be people, but no one knows for sure...')
        print('5 minutes after you`ve been deciding where to go you`ve seen blinding lights on the right...')
        ans1 = input('\nWhich way you wanna go? (left/right) ').lower()
        stage += 1
        if ans1 == 'health':
            show_health()
            ans1 = input('Enter the answer here: ').lower()
        if ans1 == 'right':
            print('\n\nCongrats, your story continues...')
            print('\nAs you run further to the lights you noticed the railway, \nbut sprained your ankle and lost 1 health in addition your speed is 2 times slower then it was before...')
            health -= 1
            show_health()
            railway()
        elif ans1 == 'left':
            print('There were witches, so they made you their slave and now you gather rare plants for their potions...')
            print('\nYou lost... Game`s over.')
            #chance += 1
            game_over = the_end()

        else:
            print('You entered an unknown word, so you lost...')
            game_over = the_end()

if age >= 12:
    print("Congrats, you may play \"Logic Episodes\" right now!")
    wish_to_play = input("Do you wanna play? (y/n) ").lower()
    if wish_to_play == 'y':
        game_over = False
        print('Let`s begin!\n')
        game()
    else:
        print('C U L8R')
        game_over = the_end()
else:
    print("Sorry, you`re too young to play this game")
    game_over = the_end()


