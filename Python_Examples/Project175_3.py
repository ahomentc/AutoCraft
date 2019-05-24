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
            <Name>Monty</Name>
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
                <RewardForTouchingBlockType>
                    <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
                    <Block reward="100.0" type="water" behaviour="onceOnly"/>
                </RewardForTouchingBlockType>
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
        self.observation_space = ['air', 'air', 'air']  # I think this is ame as our state
        # self.state             = {}
        self.steps             = 0

    def teleport(self, agent_host, teleport_x, teleport_z):
        """Directly teleport to a specific position."""
        tp_command = "tp " + str(teleport_x) + " 225 2"
        agent_host.sendCommand(tp_command)

    # def step(self, action):
    #     """ Checks for 1st choice and returns a door that is not the car door. """

    #     '''
    #     TODO: MAYBE MAKE THE REWARD DEPEND ON THE ACTUAL EVENT THAT HAPPENS IN THE GAME.
    #     LIKE YOU YOU FALL IN LAVA AND DIE. DYING GIVES A NEGATIVE REWARD.
    #     MAYBE DO THIS LATER THOUGH

    #     '''

    #     if action not in self.action_space:
    #         print("Error: action", action, "is illegal.")
    #     reward = 0
    #     if self.steps == 0:        ## 1st choice of Monty
    #         reward += 0.33
    #         self.state[action] = 1 ##chosen: state=1, not chosen: state=0, opened(by host): state=2
    #         if action == 0:
    #             if self.hidden_state[1] == 'water':  ## dirt
    #                 self.state[2] = 2
    #                 self.hidden_state[2] = 'opened'
    #             elif self.hidden_state[2] == 'water':
    #                 self.state[1] = 2
    #                 self.hidden_state[1] = 'opened'
    #         elif action == 1:
    #             if self.hidden_state[0] == 'water':
    #                 self.state[2] = 2
    #                 self.hidden_state[2] = 'opened'
    #             elif self.hidden_state[2] == 'water':
    #                 self.state[0] = 2
    #                 self.hidden_state[0] = 'opened'
    #         elif action == 2:
    #             if self.hidden_state[0] == 'water':
    #                 self.state[1] = 2
    #                 self.hidden_state[1] = 'opened'
    #             elif self.hidden_state[1] == 'water':
    #                 self.state[0] = 2
    #                 self.hidden_state[0] = 'opened'
    #     elif self.steps == 1:     ##Monty chooses a second time and computes reward
    #         for k in self.state.keys():
    #             if self.state[k] == 1:
    #                 self.state[k] = 0
    #         self.state[action] = 1
    #         total = 0
    #         for i in range(3):
    #             if self.hidden_state[i] == 'water':
    #                 total += self.state[i] - 1
    #             elif self.hidden_state[i] == 'opened':
    #                 total += self.state[i] - 2
    #             elif self.hidden_state[i] == 'lava':
    #                 total += self.state[i] - 0
    #         if total == 0:
    #             reward += 1.0
    #     self.steps+=1
    #     if self.steps == 2:  ## return state, reward, completion, {}
    #         return self.state, reward, True, {}
    #     return self.state,reward, False, {}

        # returns an index from lavaOrd of the wrong choice to reveal
    def revealOneWrongChoice(self):
        index = random.randint(0, 1)
        selections = []
        for i in range(3):
            if lavaOrd[i] == 'lava':
                selections.append(i)
        self.observation_space[selections[index]] = 'stone'
        # update the observation state to show a block
        # also place a stone --- TODO ---
        return selections[index]


    def get_possible_actions(self, agent_host):
        '''
		TODO: 
			IF FIRST ACTION SET A BLOCK AS MARKING
			IF SECOND ACTION TELEPORT TO A HOLE
        '''
        action_list = []
        # check to see which enviornment placed
        # then selects a block to teleport to
        print(self.observation_space)
        if self.observation_space[0] == 'stone':
            action_list = tuple([1,2])
        elif self.observation_space[1] == 'stone':
            action_list = tuple([0,2])
        elif self.observation_space[2] == 'stone':
            action_list = tuple([0,1])

        return action_list

    # only does the second action. Not for the first action. That one is always random anyways
    def choose_action(self, curr_state, possible_actions, eps):
        """Chooses an action according to eps-greedy policy. """
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0

        a = random.uniform(0, 1)
        if a <= eps:
            a2 = random.randint(0, len(possible_actions) - 1)
            return possible_actions[a2]
        else:
            maxTuple = max(self.q_table[curr_state].items(),key = lambda x:x[1])
            maxList = [i[0] for i in self.q_table[curr_state].items() if i[1] == maxTuple[1]]
            a2 = random.randint(0, len(maxList) - 1)
            return maxList[a2]

    def convert_code_to_world_action(self, action):
        return 2 * (action-1)

    # action will be an array, first entree identifies action type
    def act(self, agent_host, is_first_action, action):
        '''
		TODO: 
			DO THE ACTUAL ACTION. EITHER MARKING OR TELEPORTING.
			CALL "step" SOMEWHERE IN HERE
        '''
        # first action, choose to place a block
        reward = 0
        if is_first_action:
            # need to do this part so that "get_possible_actions works"
            locRepr = action.index('diamond')
            pass
        # second action, teleport
        else:
            xcoord = self.convert_code_to_world_action(action)
            self.teleport(agent_host, xcoord, 2)
            if world_state.number_of_rewards_since_last_state > 0:
                reward+= world_state.rewards[0].getValue()
        return reward


    def update_q_table(self, tau, S, A, R, T):
        '''
        TODO:
        '''
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        print("gamma:", self.gamma)
        print("R:", R)
        print("S:", S)
        print("A:", A)

        G = sum([self.gamma ** i * R[i] for i in range(len(S))])        
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]
        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)
        print("end q_table:", self.q_table)

    def get_curr_state(self):
        return tuple(self.observation_space)

    def chooseRandomFirstAction(self):
        index = random.randint(0, 2)
        self.observation_space[index] = 'diamond'
        # -- TODO -- also place the actual diamond

    def run(self, agent_host):
        '''
        TODO:
        '''
       	S, A, R = deque(), deque(), deque()

        # choose a random action (select first door)
        # we don't need to train for this as its always random
        self.chooseRandomFirstAction()

        # now place a stone to mark where lava is (presentor opening door)
        indexOfReveal = self.revealOneWrongChoice()    
        print("\nobservation space: ", self.observation_space)
        
        # we're using observation_space as the state
        s = self.get_curr_state()
        S.append(s)
        possible_actions = self.get_possible_actions(agent_host)
        next_a = self.choose_action(s, possible_actions, self.epsilon)
        A.append(next_a)
        
        # act and get reward from the action
        
        current_r = self.act(agent_host, False, A[-1]) # should there be another update q above this?
        R.append(current_r)


        
        # update the q table somehow TODO

        
        t = 2 #arbitrary number. just trying to get tau and update_q_table to work
        T = sys.maxsize #No relevance rn. just trying to get tau and update_q_table to work.
        tau = t - self.n + 1

        if t < T:
            current_r = self.act(agent_host, False, A[-1])
            R.append(current_r)
            
            s = self.get_curr_state()
            S.append(s)
            possible_actions = self.get_possible_actions(agent_host)
            next_a = self.choose_action(s, possible_actions, self.epsilon)
            A.append(next_a)
        
        if tau >= 0:
            self.update_q_table(tau, S, A, R, T)
        else:
            self.update_q_table(tau, S, A, R, T)


if __name__ == '__main__':

    print('Starting...', flush=True)

    expected_reward = 3390
    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))

    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print('ERROR:', e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        print(agent_host.getUsage())
        exit(0)
    retry = 0
    epocs = 1000
    monty = Monty()
    for epoc_num in range(1000):
        my_mission = MalmoPython.MissionSpec(GetMissionXML("Monty #" + str(epoc_num)), True)
        my_mission_record = MalmoPython.MissionRecordSpec()  # Records nothing by default
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(0)
        
        try:
            # Attempt to start the mission:
            retry+=1
            agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "monty")
            # break
        except RuntimeError as e:
            if retry == epocs - 1:
                print("Error starting mission", e)
                print("Is the game running?")
                exit(1)
            else:
                time.sleep(2)
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()

                # Every few iteration Monty will show us the best policy that he learned.
        if (epoc_num + 1) % 5 == 0:
            print((epoc_num+1), 'Showing best policy:', end = " ")
            best_policy = monty.best_policy(agent_host)
        else:
            print((epoc_num+1), 'Learning Q-Table:', end = " ")
            monty.run(agent_host=agent_host)
        lavaOrd=['lava','lava','lava']
        time.sleep(1)




