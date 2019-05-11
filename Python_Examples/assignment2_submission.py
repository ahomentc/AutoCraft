import random

# items=['pumpkin', 'sugar', 'egg', 'egg'] # original items
items=['planks', 'planks', 'pumpkin', 'sugar', 'egg', 'egg', 'red_mushroom']

food_recipes = {'pumpkin_pie': ['pumpkin', 'egg', 'sugar'],
                'pumpkin_seeds': ['pumpkin'],
                'bowl': ['planks', 'planks'],
                'mushroom_stew': ['bowl', 'red_mushroom']}

rewards_map = {'pumpkin': -5, 'egg': -25, 'sugar': -10,
               'pumpkin_pie': 100, 'pumpkin_seeds': -50,
               'bowl': -1, 'mushroom_stew':100, 
               'red_mushroom':5,'planks':-5}

def is_solution(reward):
    # return reward = 100 # number4
    return reward == 200 # number 8


def get_curr_state(items):
	tup = []
	for item,num in items:
		for _ in range(num):
			tup.append(item)
	return tuple(tup)

def choose_action(curr_state, possible_actions, eps, q_table):
	a = random.uniform(0, 1)
	if a <= eps:
		a2 = random.randint(0, len(possible_actions) - 1)
		return possible_actions[a2]
	else:
		maxTuple = max(q_table[curr_state].items(),key = lambda x:x[1])
		maxList = [i[0] for i in q_table[curr_state].items() if i[1] == maxTuple[1]]
		a2 = random.randint(0, len(maxList) - 1)
		return maxList[a2]


# 2. 5C3 + 5C2 + 5C1 + 5C0 = 10 + 10 + 5 + 1 = 26 

# 4. is 100

# 5. 40 Showing best policy: pumpkin, egg, sugar, c_pumpkin_pie, present_gift,  with reward 100.0
# Found solution
# Done

# 7. 9C3 + 9C2 + 9C1 + 9C0 = 130

# 8. 200

# 9.

# 200 Showing best policy: red_mushroom, present_gift,  with reward 5.0
# 201 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 202 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 203 Learning Q-Table: red_mushroom, planks, planks, c_bowl, sugar, c_mushroom_stew, egg, present_gift, Reward: 65
# 204 Learning Q-Table: planks, egg, pumpkin, c_pumpkin_seeds, present_gift, Reward: -80
# 205 Showing best policy: red_mushroom, present_gift,  with reward 5.0
# 206 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 207 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 208 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 209 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 210 Showing best policy: red_mushroom, present_gift,  with reward 5.0
# 211 Learning Q-Table: planks, egg, present_gift, Reward: -30
# 212 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 213 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 214 Learning Q-Table: red_mushroom, planks, present_gift, Reward: 0
# 215 Showing best policy: red_mushroom, present_gift,  with reward 5.0
# 216 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 217 Learning Q-Table: pumpkin, planks, planks, c_pumpkin_seeds, c_bowl, sugar, present_gift, Reward: -61
# 218 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 219 Learning Q-Table: red_mushroom, present_gift, Reward: 5
# 220 Showing best policy: red_mushroom, present_gift,  with reward 5.0