---
layout: default
title: Proposal
---
# AutoCraft Proposal


## Summary of the Project
The main idea behind the project is to solve the Monty Hall problem. The Monty Hall problem is a brain teaser of sorts which traditionally involves the use of probability. <br/>
The player is given 3 doors, 2 of which contains goat and the final one contains a car. The aim for the player is to win the car. The player first makes a choice, the host opens up a door (not chosen by the player) with a goat in it and provides a choice to the player to stick with his option or change his preference. <br/>
According to probability, the player should change his door to maximize his chances. The aim of this project is to make sure the agent learns to change his option of the door when prompted by the host in order to have the highest probability of winning.<br/>
Input: Observation State <br/>
Output: list of actions needed to move to door and hit the switch (some way to indicate choice)

n-1/n

##  AI/ML Algorithms
We are going to be implementing a deep Q learning algorithm that works backwards to figure out how the actions of the agent led to the final reward.

##  Evaluation Plan
We will evaluate the success of the project if the agent first selects a hole, then always switches to the unselected hole after the environment reveals the incorrect/bad hole. The Quantitative metric: (1) Agent increases success of choosing correct hole. Baselines are as followed: <br/>
(1) Agent can walk to a hole, <br/>
(2) Agent acts on a choice that gives a better reward, <br/>
(3) Agent switches to hole after environment reveals a hole that had a bad outcome, <br/>
(4) Agent continuously switches to unselected hole environment reveals a bad outcome. We expect our approach to improve the metric by at least ⅔ of the total sessions, <br/>
(5) Agent can switch to a correct hole on N amount of holes, where N is less than 100. We will evaluate the agent based on the data collected after every session that the agent completes.

<br/>
Qualitatively, the agent should <br/>
(1) be able to learn to walk, <br/>
(2) be able to mark it’s first choice on a hole, <br/>
(3) pick the higher rewarding hole. To verify the agent works, we will use an algorithm to measure the amount of sessions the agent selected correctly and divide that with the total amount of sessions ran. The moonshot case will be that the agent chooses correctly greater than n-1/n times for n number of doors.


## Appointment with the Instructor
Our meeting time is: 04:00pm - Wednesday, April 24, 2019
The meeting place is: DBH 4204

