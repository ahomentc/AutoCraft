---
layout: default
title: Status
---
# AutoCraft Status

<iframe width="560" height="315" src="https://www.youtube.com/embed/IQFVIjwp4c0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Project Summary: 
We are training an agent to learn how to solve the Monty Hall Problem. In the problem, the player is given 3 doors, 2 of which contains goat and the final one contains a car. The aim for the player is to win the car. The player first makes a choice, the host opens up a door (not chosen by the player) with a goat in it and provides a choice to the player to stick with his option or change his preference. 
According to probability, the player should change his door to maximize his chances, with a probability of 2/3 if he switches. The aim of this project is to make sure the agent learns to change his option of the door when prompted by the host in order to have the highest probability of winning.

# Approach: 
The way we emulate the problem is by having holes through which the agent can either land in lava or water. If the agent lands in lava, he dies, while if he lands in water, he survives. Regardless of how many holes there are, there will only be one that has water under it, with the rest having lava.

We are setting the observation space of the player as an array of of n 'air' elements for n holes. The, the agent places a diamond in front of his first choice, which updates the observation space. Then the environment reveals a wrong choice by placing a stone in front of another hole, which also updates the observation space. The observation space is now the state and the agent searches the q table for it and updates the entree based on the reward it recieve from selecting an action. The action being which hole to teleport to.

<br/>
<img src="https://i.imgur.com/8mJo2v0.png" alt="drawing" width="600"/><br/>
In this example iteration, you can see what the q-table looks like. In addition you can see a 2D representation of the enviornment on top. The top row of the table shows the action enviornment. The second row show the markings that the agent and enviornment have made (observation state) and the third row shows the action. You can also see the reward given for the state and action. 

We are using an epsilon of .05 so random selections are relevivly infrequent. 
The number of states depends on the number of holes, there are n! states for n holes.
There are only two actions, either the agent selects the first choice, or chooses to switch to the only remaining non-revealed option.

We reward the agent for landing on water, which is to choose correctly and give negative reward for landing in lava.

We are using the q-learning algorithm to train the agent to select the correct choice. The equation is
q_table[State][Action] += alpha * ((gamma * Reward  + gamma * n * q_table[State][Action]) - q_table[State][Action]) 

# Evaluation: 
For each number of doors, we run the algorithm but make the agent always land in water. During those iterations, we calculate the number of times the choice to switch would have led to survival. We could have done this by math as well with the equation being [% survive if switch = n-1/n] but we wanted to test in the enviornment as well.

For n=3 doors, we recieved .6 in our benchmark. When we ran our algorithm, we found our agent mostly stayed around .6 for the amount of time it decided to switch, which is good. The agent survived around 60 percent of the time which is good because it is close to the real probability for the problem.

<br/>
<img src="https://i.imgur.com/Q6OZgxO.png" alt="drawing" width="600"/><br/>
Screenshot for 3 holes<br/>

For n=5 doors, we recieved .8 in our benchmark. When we ran our algorithm, we found our agent mostly stayed around .8 for the amount of time it decided to switch, which is good. The agent only survived around 60% of the time which is not great given that the probability of survival should be closer to 80%.

<br/>
<img src="https://i.imgur.com/u89oSr2.png" alt="drawing" width="600"/><br/>
Screenshot for 5 holes<br/>

Our algorithm works decently well with probability of switching the agent's choice equal to the probability of being correct if switches.

However, we want to make the agent always switch, but it is tough because there are rounds where it is unlucky for that in that the correct choice would be to not switch. This is counteracted by having more holes, but the more doors we have, the longer it takes to train. The complexity for increasing the number of states is O(n^n) so it gets out of hand quickly.

We wanted our percent of switching to be closer to 100%, regardless of what our baseline is. We did this by making the states in the q-table being only diamond and air and by making abs(positive reward) > abs(negative reward). When this worked well, we recieved around 90% of time it switching which was great, however the values for the entrees in the q table would sometimes both sprial downwards negativly with no clear choice.

<br/>
<img src="https://i.imgur.com/ok9ZNaq.png" alt="drawing" width="600"/><br/>
Screenshot where new technique goes really well<br/>

<img src="https://i.imgur.com/xQd3PYV.png" alt="drawing" width="600"/><br/>
Screenshot where new technique goes really bad<br/>

# Remaining Goals and Challenges
So far our algorithm works decently well with probability of switching the agent's choice equal to the probability of being correct if switches. We want to surpase the limitation that we get from the probability of choosing correctly if the agent switches. This may be tough given how the probability of the Monty Hall Problem is. As a metaphor, if there are two buttons, and one always kills the agent while the other rewards, it is trivial to train the agent. However, in our case, each button would have a probability of killing the agent instead of 100% and we are limited to train based on those probabilities. However, we want to surpass this limitation.

In the next 2-3 weeks, we are going to attempt to make the agent almost always switch doors, regardless of the probability that impedes this. There are a couple of ways we can do this: Use more doors, Keep it running longer, Make it run faster, Change our q table, Change how we update our q table. 

If we decide to use more doors, we'll have to somehow make the algorithm run faster or change it so that it isn't complexity n^n. I think that if we combine having more doors, with having the states only be "switching" and "not switching", and more positive rewards than negative, we'll be able to reduce the huge size of the q table that occurs when there are many states. This might also handle the problems that having only two states in the q table created. 

We will also experiment with using a Sequential NN to choose the action. 

# Resources Used:
https://towardsdatascience.com/deep-learning-a-monty-hall-strategy-or-a-gentle-introduction-to-deep-q-learning-and-openai-gym-d66918ac5b26

https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

https://www.freecodecamp.org/news/an-introduction-to-q-learning-reinforcement-learning-14ac0b4493cc/


