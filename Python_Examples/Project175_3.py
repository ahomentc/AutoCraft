from __future__ import division
import numpy as np

import MalmoPython
import os
from random import randint
import sys
import time
import json
import random
import math
import errno
import Project175_helper as submission
from collections import defaultdict, deque
from timeit import default_timer as timer
from secrets import randbelow

import torch
import torch.nn as nn

items=['dirt', 'diamond']

lavaOrd=['lava','lava','lava'] # hidden state

# randomly set lava to two locations and dirt to one
def setCorrectLoc():
	correctLoc = randbelow(3)
	print(correctLoc)
	lavaOrd[correctLoc] = 'dirt'

# get coordinates of the lava
def getLavaPositions():
    positions = [] # [(x,y,z),(x,y,z)]
    for i,ele in enumerate(lavaOrd):
    	if ele == 'lava':
    		x = -2 + (i*2)
    		y = 225
    		z = 2
    		positions.append((x,y,z))
    return positions

def getDirtPosition():
    position = ()
    for i,ele in enumerate(lavaOrd):
        if ele == 'dirt':
            x = -2 + (i*2)
            y = 225
            z = 2
            position = (x,y,z)
    return position

# create the XML for the lava
def getLavaDrawing(positions):
	drawing = ""
	for p in positions:
		drawing += '<DrawBlock x="' + str(p[0]) + '" y="' + str(p[1]) + '" z="' + str(p[2]) + '" type="lava" />'
	print(drawing)
	return drawing

def getDirtDrawing(position):
    return '<DrawBlock x="' + str(position[0]) + '" y="' + str(position[1]) + '" z="' + str(position[2]) + '" type="water" />'

# returns an index from lavaOrd of the wrong choice to reveal
def revealOneWrongChoice():
	occurance = random.randint(0, 2)
	# select either first occurance or second of lavaOrd
	for i in range(3):
		if occurance == 0 and lavaOrd[i] == 'lava':
			return i
		else:
			occurance-=1


def GetMissionXML(summary):
    ''' Build an XML mission string that uses the RewardForCollectingItem mission handler.'''

    setCorrectLoc()
    lava_positions = getLavaPositions()
    dirt_position = getDirtPosition()

    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + summary + '''</Summary>
        </About>

        <ModSettings>
            <MsPerTick>100</MsPerTick>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
                <DrawingDecorator>
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-3" y1="240" z1="-3" x2="3" y2="240" z2="3" type="stone" />
                    
                    <DrawBlock x="2" y="240" z="2" type="air"/>
                    <DrawBlock x="0" y="240" z="2" type="air"/>
                    <DrawBlock x="-2" y="240" z="2" type="air"/>

                    <DrawBlock x="2" y="240" z="1" type="air"/>
                    <DrawBlock x="0" y="240" z="1" type="air"/>
                    <DrawBlock x="-2" y="240" z="1" type="air"/>
                    <DrawBlock x="2" y="239" z="1" type="stone"/>
                    <DrawBlock x="0" y="239" z="1" type="stone"/>
                    <DrawBlock x="-2" y="239" z="1" type="stone"/>

                    ''' + getLavaDrawing(lava_positions) + getDirtDrawing(dirt_position) + '''
                    
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Odie</Name>
            <AgentStart>
                <Placement x="0" y="241.0" z="0"/>
                <Inventory>
                    <InventoryItem slot="9" type="dirt" />
                    <InventoryItem slot="10" type="diamond"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <AbsoluteMovementCommands/>
                <SimpleCraftCommands/>
                <MissionQuitCommands/>
                <InventoryCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullInventory/>
                <AgentQuitFromCollectingItem>
                    <Item type="rabbit_stew" description="Supper's Up!!"/>
                </AgentQuitFromCollectingItem>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

class Monty(object):
    def __init__(self, alpha=0.3, gamma=1, n=1):
        """Constructing an RL agent.

        Args
            alpha:  <float>  learning rate      (default = 0.3)
            gamma:  <float>  value decay rate   (default = 1)
            n:      <int>    number of back steps to update (default = 1)
        """
        self.epsilon = 0.2  # chance of taking a random action instead of the best
        self.q_table = {}
        self.n, self.alpha, self.gamma = n, alpha, gamma

        # ------- Init the environment stuff here ----
        # ex:
        self.hidden_state      = lavaOrd     #would be better to take this as an argument
        self.action_space      = [0, 1, 2]   #which door
        #self.observation_space = ['air', 'air', 'air'] Not needed???? Prob not
        self.state             = {}
        self.steps             = 0

    def teleport(self, agent_host, teleport_x, teleport_z):
        """Directly teleport to a specific position."""
        tp_command = "tp " + str(teleport_x)+ " 226 " + str(teleport_z)
        agent_host.sendCommand(tp_command)
        good_frame = False
        start = timer()
        while not good_frame:
            world_state = agent_host.getWorldState()
            if not world_state.is_mission_running:
                print("Mission ended prematurely - error.")
                exit(1)
            if not good_frame and world_state.number_of_video_frames_since_last_state > 0:
                frame_x = world_state.video_frames[-1].xPos
                frame_z = world_state.video_frames[-1].zPos
                if math.fabs(frame_x - teleport_x) < 0.001 and math.fabs(frame_z - teleport_z) < 0.001:
                    good_frame = True
                    end_frame = timer()

    def step(self, action):
        """ Checks for 1st choice and returns a door that is not the car door. """

        '''
        TODO: MAYBE MAKE THE REWARD DEPEND ON THE ACTUAL EVENT THAT HAPPENS IN THE GAME.
        LIKE YOU YOU FALL IN LAVA AND DIE. DYING GIVES A NEGATIVE REWARD.
        MAYBE DO THIS LATER THOUGH

        '''

        if action not in self.action_space:
            print("Error: action", action, "is illegal.")
        reward = 0
        if self.steps == 0:        ## 1st choice of Monty
            reward += 0.33
            self.state[action] = 1 ##chosen: state=1, not chosen: state=0, opened(by host): state=2
            if action == 0:
                if self.hidden_state[1] == 'water':  ## dirt
                    self.state[2] = 2
                    self.hidden_state[2] = 'opened'
                elif self.hidden_state[2] == 'water':
                    self.state[1] = 2
                    self.hidden_state[1] = 'opened'
            elif action == 1:
                if self.hidden_state[0] == 'water':
                    self.state[2] = 2
                    self.hidden_state[2] = 'opened'
                elif self.hidden_state[2] == 'water':
                    self.state[0] = 2
                    self.hidden_state[0] = 'opened'
            elif action == 2:
                if self.hidden_state[0] == 'water':
                    self.state[1] = 2
                    self.hidden_state[1] = 'opened'
                elif self.hidden_state[1] == 'water':
                    self.state[0] = 2
                    self.hidden_state[0] = 'opened'
        elif self.steps == 1:     ##Monty chooses a second time and computes reward
            for k in self.state.keys():
                if self.state[k] == 1:
                    self.state[k] = 0
            self.state[action] = 1
            total = 0
            for i in range(3):
                if self.hidden_state[i] == 'water':
                    total += self.state[i] - 1
                elif self.hidden_state[i] == 'opened':
                    total += self.state[i] - 2
                elif self.hidden_state[i] == 'lava':
                    total += self.state[i] - 0
            if total == 0:
                reward += 1.0
        self.steps+=1
        if self.steps == 2:  ## return state, reward, completion, {}
            return self.state, reward, True, {}
        return self.state,reward, False, {}


    def get_possible_actions(self, agent_host, is_first_action=False):
        '''
		TODO: 
			IF FIRST ACTION SET A BLOCK AS MARKING
			IF SECOND ACTION TELEPORT TO A HOLE
        '''

    def choose_action(self, curr_state, possible_actions, eps):
        """Chooses an action according to eps-greedy policy. """
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0

        return submission.choose_action(curr_state, possible_actions, eps, self.q_table)

    def act(self, agent_host, action):
        '''
		TODO: 
			DO THE ACTUAL ACTION. EITHER MARKING OR TELEPORTING.
			CALL "step" SOMEWHERE IN HERE
        '''

    def update_q_table(self, tau, S, A, R, T):
        '''
        TODO:
        '''
        pass

    def run(self, agent_host):
        '''
        TODO:
        '''
       	pass


if __name__ == '__main__':
	'''
	GET IT TO WORK SOMEHOW
	'''
    model = DQN(len(env.observation_space), len(env.action_space))
    epocs = 1000
    for epoc_num in range(epocs):
        # epsilon = epsilon_by_frame(frame_idx)
        # action = model.act(state, epsilon)
        # next_state, reward, done, _ = env.step(int(action))
        my_mission = MalmoPython.MissionSpec(GetMissionXML("Monty #" + str(epoc_num)), True)
        try:
            # Attempt to start the mission:
            agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "Odie")
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission", e)
                print("Is the game running?")
                exit(1)
            else:
                time.sleep(2)
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()





