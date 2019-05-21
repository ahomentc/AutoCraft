"""
Odie is trying to get the best present. Help him to learn what he should do.

Author: Moshe Lichman and Sameer Singh
"""
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


class DQN(nn.Module):

    # sequential nn with 3 inputs 3 outputs
    # also performing dropout to decrease overfit
    def __init__(self, num_inputs, num_outputs):
        super(DQN, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(num_inputs, 30),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(30, num_outputs)
        )

    def forward(self, x):
        return self.layers(x)

    def act(self, state, eps):
        rand = random.random()
        if rand < eps: # epsilon random
            return random.randrange(env.action_space.n) # returning random number in range of the number of actions available
        else:
            s = Variable(torch.FloatTensor(state))
            qValue = self.forward(s)
            return qValue.max(1)[1] # returns the max action from the nn output


# need a way to map from lavaOrd and items to map coordinates

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
        self.inventory = defaultdict(lambda: 0, {})
        self.num_items_in_inv = 0

        # ------- Init the environment stuff here ----
        # ex:
        self.hidden_state      = lavaOrd     #would be better to take this as an argument
        self.action_space      = [0, 1, 2]   #which door
        #self.observation_space = ['air', 'air', 'air'] Not needed????
        self.state             = {}
        self.steps             = 0


    def clear_inventory(self):
        """Resets the inventory in case of a new attempt to fetch. """
        self.inventory = defaultdict(lambda: 0, {})
        self.num_items_in_inv = 0


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


    def present_gift(self, agent_host):
        """Calculates the reward points for the current inventory.

        Args
            agent_host: the host object

        Returns
            reward:     <float> current reward from world state
        """
        current_r = 0
        #time.sleep(0.1)

        for item, counts in self.inventory.items():
            current_r += rewards_map[item] * counts

        agent_host.sendCommand('quit')
        #time.sleep(0.25)
        return current_r


    @staticmethod
    def is_solution(reward):
        """If the reward equals to the maximum reward possible returns True, False otherwise. """
        return submission.is_solution(reward)

    def get_possible_actions(self, agent_host, is_first_action=False):
        """Returns all possible actions that can be done at the current state. """
        action_list = []
        if not is_first_action:
            # Not allowing Odie to come back empty.
            action_list = ['present_gift']

        craft_opt = self.get_crafting_options()
        if len(craft_opt) > 0:
            action_list.extend(['c_%s' % craft_item for craft_item in craft_opt])

        if self.num_items_in_inv < inventory_limit:
            nearby_obj = self.get_obj_locations(agent_host)
            if len(nearby_obj) > 1:
                action_list.extend([item for item in nearby_obj.keys() if item != 'Odie'])

        return action_list

    def get_curr_state(self):
        """Creates a unique identifier for a state.

        The state is defined as the items in the agent inventory. Notice that the state has to be sorted -- otherwise
        differnt order in the inventory will be different states.
        """
        return submission.get_curr_state(self.inventory.items())

    def choose_action(self, curr_state, possible_actions, eps):
        """Chooses an action according to eps-greedy policy. """
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0

        return submission.choose_action(curr_state, possible_actions, eps, self.q_table)

    def act(self, agent_host, action):
        print(action + ",", end = " ")
        if action == 'present_gift':
            return self.present_gift(agent_host)
        elif action.startswith('c_'):
            self.craft_item(agent_host, action[2:])
        else:
            self.fetch_item(agent_host, action)

        return 0

    def update_q_table(self, tau, S, A, R, T):
        """Performs relevant updates for state tau.

        Args
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
        """
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

    def best_policy(self, agent_host):
        """Reconstructs the best action list according to the greedy policy. """
        self.clear_inventory()
        policy = []
        current_r = 0
        is_first_action = True
        next_a = ""
        while next_a != "present_gift":
            curr_state = self.get_curr_state()
            possible_actions = self.get_possible_actions(agent_host, is_first_action)
            next_a = self.choose_action(curr_state, possible_actions, 0)
            policy.append(next_a)
            is_first_action = False
            current_r = self.act(agent_host, next_a)
        print(' with reward %.1f' % (current_r))
        return self.is_solution(current_r)
        #print 'Best policy so far is %s with reward %.1f' % (policy, current_r)

    def run(self, agent_host):
        """Learns the process to compile the best gift for dad. """
        S, A, R = deque(), deque(), deque()
        present_reward = 0
        done_update = False
        while not done_update:
            s0 = self.get_curr_state()
            possible_actions = self.get_possible_actions(agent_host, True)
            a0 = self.choose_action(s0, possible_actions, self.epsilon)
            S.append(s0)
            A.append(a0)
            R.append(0)

            T = sys.maxsize
            for t in range(sys.maxsize):
                time.sleep(0.1)
                if t < T:
                    current_r = self.act(agent_host, A[-1])
                    R.append(current_r)

                    if A[-1] == "present_gift":
                        # Terminating state
                        T = t + 1
                        S.append('Term State')
                        present_reward = current_r
                        print("Reward:", present_reward)
                    else:
                        s = self.get_curr_state()
                        S.append(s)
                        possible_actions = self.get_possible_actions(agent_host)
                        next_a = self.choose_action(s, possible_actions, self.epsilon)
                        A.append(next_a)

                tau = t - self.n + 1
                if tau >= 0:
                    self.update_q_table(tau, S, A, R, T)

                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break

if __name__ == '__main__':

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



    # -------- ASSIGNMENT 2 BELOW ---------


    #sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
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

    num_reps = 30000
    n=1
    odie = Odie(n=n)
    print("n=",n)
    odie.clear_inventory()
    for iRepeat in range(num_reps):
        my_mission = MalmoPython.MissionSpec(GetMissionXML("Fetch boy #" + str(iRepeat)), True)
        my_mission_record = MalmoPython.MissionRecordSpec()  # Records nothing by default
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(0)
        max_retries = 3
        for retry in range(max_retries):
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

        # Every few iteration Odie will show us the best policy that he learned.
        if (iRepeat + 1) % 5 == 0:
            print((iRepeat+1), 'Showing best policy:', end = " ")
            found_solution = odie.best_policy(agent_host)
            if found_solution:
                print('Found solution')
                print('Done')
                break
        else:
            print((iRepeat+1), 'Learning Q-Table:', end = " ")
            # odie.run(agent_host)

        odie.clear_inventory()
        time.sleep(1)


