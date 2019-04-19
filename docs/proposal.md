---
layout: default
title: Proposal
---
# AutoCraft Proposal


## Summary of the Project
In this project, we plan to create an agent that avoid/resists enemies. The approach of the agent will be to avoid hostile attacks and damages by building structures to defend itself. 

To measure the performance of our agent we will gudge it on the following terms: \n
Positive feedback for: \n
	- Surviving. More time = More reward \n
Negavite feedback for: \n
	- Getting hit \n
	- Dying \n
	- Placing blocks (to encourage efficent design) \n

The environment we will be using for this project will be a controlled one where zombies are respawned after a fixed amount of time or by user input. We will set the number of zombies ourselves.


##  AI/ML Algorithms
We will use Reinforcement learning with Q-learning. 

##  Evaluation Plan
We plan to evaluate the agent based on how long it can stay alive and its health level. The longer it stays alive, the higher the score. Similarly for health, higher health will be rewarded. We will run the ML algorithm until the difference in time between the previous survival length and the current surival length is less than 1 second. 

The base goal is to survive with a single zombie on a flat plain. The next goal will be to survive against 3 enemies of different types at the same time. The final goal will be to survive against 10 enemies.

Our time goal will be to make agent survive for at least three minutes for each goal.


## Appointment with the Instructor
Our meeting time is: 04:00pm - Wednesday, April 24, 2019
The meeting place is: DBH 4204

