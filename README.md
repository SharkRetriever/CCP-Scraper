# CanadianCubing Psych Scraper #

## What is it? ##

A web scraper that generates psych sheets for CanadianCubing speedcubing competitions.  
Speedcubing is a hobby where solvers attempt to solve the Rubik's cube (and related twisty puzzles) as quickly as they can.

The psych sheet lists a ranking of solvers along with their best times in that event.  
For blindfolded events, the best time is their best recorded single.  
For other events, the best time is their best recorded average. If they do not have one, then it is their best recorded single.  
Note that for all events, if the single time is listed, the string "(s)" follows the time


## How do you run it? ##

For the programmers:

- clone the repository
- source venv/bin/activate
- python3 main.py
- ???
- NCR 2017 Psych Sheet! Or whatever CanadianCubing competition you asked for


## How reliable are the results? ##

The scraper only considers people who have competed before. Even then, a competitor's performance can vary unexpectedly. Thus, consider a standard deviation of around 5 spots.

Warning: Do not bet with this program.
