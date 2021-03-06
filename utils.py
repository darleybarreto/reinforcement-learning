from games import *
import os

games ={1:["FlappyBird", flappybird],\
        2:["Pong",pong],\
        3:["Catcher",catcher],\
        4:["Snake",snake],\
        5:["PuckWorld",puckworld],\
        6:["Pixelcopter",pixelcopter],\
        7:["Quit"]}

mode = {1: "Train", 2: "Test", 3:"Quit"} 

def menu():
    while True:
        os.system('clear')
        print("Select a game:")
        
        for k in games:
            print(k, games[k][0])

        op = input()
        
        try:
            op = int(op)
        except Exception as e:
            continue

        game = games.get(op,None)
        
        if not game:
            continue

        if game[0] == "Go back":
            os.system('clear')
            # sys.exit()
            return None, None
        break
    os.system('clear')

    return sub_menu(game)

def sub_menu(game):
    while True:
        os.system('clear')
        print("Select a mode:")
        
        for k in mode:
            print(k, mode[k])

        op = input()
        
        try:
            op = int(op)
        except Exception as e:
            continue

        opt = mode.get(op,None)
        
        if not opt:
            continue

        if opt == "Go back":
            os.system('clear')
            # sys.exit()
            return None,None
        
        break
    os.system('clear')

    return game, opt.lower()
