---
layout: default
title:  Home
---
<img src="http://www.sciencemadesimple.co.uk/files/2016/04/The-choices.png" alt="drawing" width="100%"/><br/>

## The Monthy Hall Problem
Source code: [https://github.com/ahomentc/AutoCraft](https://github.com/ahomentc/AutoCraft)

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)

The Monty Hall Problem is described as this: "Suppose you're on a game show, and you're given the choice of three doors: Behind one door is a car; behind the others, goats. You pick a door, say No. 1, and the host, who knows what's behind the doors, opens another door, say No. 3, which has a goat. He then says to you, "Do you want to pick door No. 2?" Is it to your advantage to switch your choice?"

Under the standard assumptions, contestants who switch have a 2/3 chance of winning the car, while contestants who stick to their initial choice have only a 1/3 chance.

A key insight is that switching doors is a different action than choosing between the two remaining doors at random, as the first action uses the previous information and the latter does not. Other possible behaviors than the one described can reveal different additional information, or none at all, and yield different probabilities.

Video describing the problem: https://www.youtube.com/watch?v=4Lb-6rxZxx0

### We are training an agent to choose to switch as much as possible

