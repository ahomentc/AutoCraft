import random

# items=['pumpkin', 'sugar', 'egg', 'egg'] # original items
items=['pumpkin', 'sugar', 'egg', 'egg', 'red_mushroom', 'planks', 'planks']

food_recipes = {'pumpkin_pie': ['pumpkin', 'egg', 'sugar'],
                'pumpkin_seeds': ['pumpkin'],
                'bowl': ['planks', 'planks'],
                'mushroom_stew': ['bowl', 'red_mushroom']}

rewards_map = {'pumpkin': -5, 'egg': -25, 'sugar': -10,
               'pumpkin_pie': 100, 'pumpkin_seeds': -50,
               'bowl': -1, 'mushroom_stew':100, 
               'red_mushroom':5,'planks':-5}

def is_solution(reward):
    # return reward == 100 # number4
    return reward == 205 # number 8


def get_curr_state(items):
	tup = []
	for item,num in items:
		for _ in range(num):
			tup.append(item)
	print("\n---")
	print(tuple(tup))
	print("-----\n")
	return tuple(tup)

def choose_action(curr_state, possible_actions, eps, q_table):
	rnd = random.random()
	a = random.randint(0, len(possible_actions) - 1)
	if a <= .2:
		return possible_actions[a]
	else:
		maxTuple = max(q_table[curr_state].items(),key = lambda x:x[1])
		maxList = [i[0] for i in q_table[curr_state].items() if i[1] == maxTuple[1]]
		a2 = random.randint(0, len(maxList) - 1)
		return maxList[a2]