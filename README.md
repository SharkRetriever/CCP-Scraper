# CCP-Scraper #

## What is it? ##

CCP-Scraper is a web scraper that generates psych sheets for CanadianCubing speedcubing competitions.
The psych sheet in this case lists a ranking of solvers along with their best average in that event.
Speedcubing is a hobby where solvers attempt to solve the Rubik's cube (and related twisty puzzles) as quickly as they can.

## How do you run it? ##

For the programmers:

- clone the repository
- use venv to set up a virtual environment and pip within the virtual environment to install from requirements.txt
- python3 main.py > test.txt
- ??? (it takes a while to scan the pages)
- NCR 2017 Psych Sheet! Or whatever CanadianCubing competition's listed inside 

## How reliable are the results? ##

The scraper only considers people who have competed before and who have an official non-DNF average in the event.
Thus, consider a standard deviation from around 4 spots for fast solvers to around 8 spots for slower solvers.

Note: Do NOT use this scraper to bet on potential winners in future competitions.
