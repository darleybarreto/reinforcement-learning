import math
import random
import pyautogui
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

opt =   {
            "Adam": torch.optim.Adam,\
            "RMSprop": torch.optim.RMSprop,\
            "SGD": torch.optim.SGD 
        }

class DQN(nn.Module):
    def __init__(self, actions, shape, fc):
        super(DQN, self).__init__()

        # that there are no pooling layers
        # pooling layers buys translation invariance:
        # the network becomes insensitive to the location of an object in the image.
        # That makes perfectly sense for a classification task like ImageNet.
        # But for games the location of an object is crucial in determining the potential reward

        in_, out_, kernel, stride = (list(zip(*shape))[i] for i in range(len(shape) + 1))
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_[0], out_[0], kernel_size=kernel[0], stride=stride[0]), 
            nn.BatchNorm2d(out_[0]),
            nn.ReLU())

        self.layer2 = nn.Sequential(
            nn.Conv2d(in_[1], out_[1], kernel_size=kernel[1], stride=stride[1]), 
            nn.BatchNorm2d(out_[1]),
            nn.ReLU())

        self.layer3 = nn.Sequential(
            nn.Conv2d(in_[2], out_[2], kernel_size=kernel[2], stride=stride[2]), 
            nn.BatchNorm2d(out_[2]),
            nn.ReLU())

        self.fc1 = nn.Linear(fc[0], fc[1])
        self.fc2 = nn.Linear(fc[1], actions)
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)

        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x

def create_model(actions, shape, fully_connected, learning_rate=1e-2, opt_='RMSprop', **kwargs):
	
    BATCH_SIZE  = kwargs.get("BATCH_SIZE",128)
    GAMMA       = kwargs.get("GAMMA", 0.999)
    EPS_START   = kwargs.get("EPS_START", 0.9)
    EPS_END     = kwargs.get("EPS_END", 0.05)
    EPS_DECAY   = kwargs.get("EPS_DECAY", 200)
    path        = kwargs.get("path", None)
    
    dqn = DQN(actions, shape, fully_connected)

    if path: load_model(path)
	
    optimizer = opt[opt_](dqn.parameters(), lr=learning_rate)
    steps_done = 0
    
    def select_greddy_action(state):
        nonlocal steps_done
        
        sample = random.random()

        eps_threshold = EPS_END + (EPS_START - EPS_END) * \
            math.exp(-1. * steps_done / EPS_DECAY)
        steps_done += 1
        
        if sample > eps_threshold:
            state = torch.from_numpy(state).float().unsqueeze(0)
            probs = dqn(Variable(state))
            # action = probs.multinomial()
            return action.data.max(1)[1].cpu() # get the index of the max log-probability

        else:
            return torch.IntTensor([[random.randrange(actions)]])

    def perform_action(possible_actions, action):
        pyautogui.press(possible_actions[action])

    def optimize():
        pass

    def save_model(path):
        if path: torch.save(dqn.state_dict(),path)

    def load_model(path): 
        dqn.load_state_dict(torch.load(path))

    return select_greddy_action, perform_action, optimize, save_model
	