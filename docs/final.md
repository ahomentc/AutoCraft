---
layout: default
title: Status
---
# AutoCraft Final Report

<iframe width="560" height="315" src="https://www.youtube.com/embed/WjNfNQ-Mj7Y" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Project Summary: 
We are training an agent to learn how to solve the Monty Hall Problem. In the problem, the player is given 3 doors, 2 of which contains goat and the final one contains a car. The aim for the player is to win the car. The player first makes a choice, the host opens up a door (not chosen by the player) with a goat in it, and offers the player the chance to switch his choice.

According to probability, the player should swtich his choice to maximize his chances of winning, with a probability of 2/3 if he switches. The aim of this project is to make sure that the agent learns to switch from his first choice when prompted by the host, in order to have the highest probability of winning.

We needed to use Reinforcement learning for this problem because it is seemingly irrational and unclear as to which door to choose. Intuitivly, people do not switch because they don't see the probability of switching as being higher, and see switching as a "trick" for them to choose the wrong door. Also, humans assume that "two choices means 50-50 chances", which is not the case. If a human was to play our program, they would most likley choose to not switch, which is wrong. We wanted to train an AI to not have that bias and choose purely based on the rewards for switching or not switching.


# Approach: 
The way we emulate the problem is by having holes through which the agent can either land in lava or water. If the agent lands in lava, he dies, while if he lands in water, he survives. Regardless of how many holes there are, there will only be one that has water under it, with the rest having lava.

We have two main approaches, one that worked and one that didn't work.

<br/> --- Approach 1 (Didn't work) --- <br/>
We are setting the observation space of the player as an array of of n 'air' elements for n holes. The, the agent places a diamond in front of his first choice, which updates the observation space. Then the environment reveals a wrong choice by placing a stone in front of another hole, which also updates the observation space. The observation space is now the state and the agent searches the q table for it and updates the entree based on the reward it recieves from selecting an action. The action being which hole to teleport to.

<br/>
<img src="https://i.imgur.com/8mJo2v0.png" alt="drawing" width="600"/><br/>
In this example iteration, you can see what the q-table looks like. In addition you can see a 2D representation of the enviornment on top. The top row of the table shows the action environment. The second row shows the markings that the agent and environment have made (observation state) and the third row shows the action. You can also see the reward given for the state and action. 

We were using an epsilon of .05 so random selections are relevivly infrequent. 
The number of states depends on the number of holes, there are n! states for n holes.
There are only two actions, either the agent selects the first choice, or chooses to switch to the only remaining non-revealed option.

We reward the agent for landing on water, which is to choose correctly and give negative reward for landing in lava.

We are using the q-learning algorithm to train the agent to select the correct choice. The equation is
q_table[State][Action] += alpha * ((gamma * Reward  + gamma * n * q_table[State][Action]) - q_table[State][Action]) 

The problem with this approach is that, for 3 doors, the agent would only survive at an average 66% maximum if he switched. So the agent was learning to switch 66% of the time. Also, it would take a large amount of time to train when the number of doors was increased, as it would make the state much much bigger.

<br/> --- Approach 2 (Worked) --- <br/>
In our proposal, we outlined a potential approach that was to change the state in the q table from being the observation space, to just "air" and "diamond". This would dramatically reduce our q table size as there would be only two entrees. 

The q table now looks like this: q_table: {'air': value, 'diamond': value}
with air representing "switch" and diamond representing "don't switch"

In our "update_q_table" function we change a key piece of code to this:
"self.q_table[ele] = old_q + self.alpha * (G - old_q)". What this is doing is to update the q table under the element (ele) that was selected for the action. Thus, the rewards would go to the element we choose to teleport to as the action. We are no longer updating based on observation space, but based on the element chosen (air or diamond, which is to switch or not switch). We also had reward for water at 10 and for lava as -9.

This was giving us some problems, which we'll address in the next section. In short, sometimes the entree in the q tables (switching or not switching) would go in a race towards negative infinity, leading to no clear choice. We solved this problem by adding an extra part called "penalizeCompetitor." What this piece of code did was that when one entree in the q table had a positive reward, the other would have a negative reward, and vice versa. The reasoning for this was that the agent would always choose the state with the highest value in the q table. And the rewards aren't always positive, even when switching. So since one action was always chosen over the other when it was ahead, sometimes the rewards had no impact because it would eventually converge to the other state's value. This would lead to a race towards negative infinity. By giving the opposite reward to the other state that wasn't chosen, this race was avoided as the rewards would always have an impact on BOTH states.

This is our update_q_table code:
	
~~~~
ele = self.observation_space[A]

# give state (ele) the reward
G = self.gamma * R   
if tau + self.n < T:
    G += self.gamma * self.n * self.q_table[ele]
old_q = self.q_table[ele]
self.q_table[ele] = old_q + self.alpha * (G - old_q)

# give other state opposite reward
if penalizeCompetitor:
    for e in self.q_table:
        if e != ele:
            G = self.gamma * R * -1   
            if tau + self.n < T:
                G += self.gamma * self.n * self.q_table[e]
            old_q = self.q_table[e]
            self.q_table[e] = old_q + self.alpha * (G - old_q)
~~~~


# Evaluation: 

There are multiple ways to get the correct solution to the Monty Hall Problem mathimatically. It can be done through Conditional Probability, Bayes's Theorem, Direct Calculation, Strategic dominance, and Simulation.

With conditional probability, the graph of the problem looks like this:
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Monty_tree_door1.svg/700px-Monty_tree_door1.svg.png" alt="drawing" width="600"/><br/>
The conditional probability of winning by switching is 
(1/3) / (1/3 + 1/6) which is 2/3 which is .66%. This was our baseline and what we strived for. Additionally, we wanted to swtich 100% of the time.


Previously, our algorithm worked decently well with probability of switching the agent's choice equal to the probability of being correct if switching. However, since the probability of being correct if switching was 66%, the agent wouldn't switch every time but would switch only 66% of the time.

We wanted our percent of switching to be closer to 100%, regardless of what the probability of being correct was. We did this by making the states in the q-table being only diamond and air and by making abs(positive reward) > abs(negative reward). When this worked well, it would switch 100% of the time, however sometimes the values for the entrees in the q table would sometimes both sprial downwards negativly with no clear choice.

<img src="https://i.imgur.com/xQd3PYV.png" alt="drawing" width="600"/><br/>
Screenshot where new technique goes really bad<br/>

We fixed this by implementing an opposite reward to the other action not taken, as described above. This second implementation wasn't immediatly clear but is much nicer because it is simpler, more elegant, and actually works and converges to swtiching 100% of the time.
Our goal, originally, was to reach a survival rate of about 66% and switch 100% of the time. As shown in the picture below, our agent had survived 63.9% of the time. It isn't 66% because of the random actions that it sometimes takes. In addition, at iteration 132 it had switched every time in the last 20 iterations. The total switching percentage is 87.9% because it also factors in the beginning iterations where it hadn't yet learned to switch. 
<img src="https://i.imgur.com/xx9szKh.png" alt="drawing" width="600"/><br/>

So we can see that this approach was a clear success. It learns to swtich 100% of the time and has the survival rate of about what is mathametically proven as the maximum.

# Resources Used:
https://towardsdatascience.com/deep-learning-a-monty-hall-strategy-or-a-gentle-introduction-to-deep-q-learning-and-openai-gym-d66918ac5b26

https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

https://www.freecodecamp.org/news/an-introduction-to-q-learning-reinforcement-learning-14ac0b4493cc/


