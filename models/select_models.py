from . import dqn
from . import a3c
import os
import sys

models ={1:["Simple DQN", dqn.run],\
        2:["Asynchronous Advantage Actor Citic",a3c.run],\
        3:["Quit"]}

def menu():
    while True:
        os.system('clear')
        print("Select a model:")
        
        for k in models:
            print(k, models[k][0])

        op = input()
        
        try:
            op = int(op)
        except Exception as e:
            continue

        model = models.get(op,None)
        
        if not model:
            continue

        if model[0] == "Quit":
            os.system('clear')
            sys.exit()
        
        break
    os.system('clear')
    return op

def select_models(**kwargs):
    
    while True:
        model = models.get(menu())[1]
        game, opt = model.menu()
        if game:
            break
    
    model.main(game, opt,**kwargs)

