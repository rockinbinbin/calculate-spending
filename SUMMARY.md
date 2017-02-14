
EVEN FINANCIAL PLANNER
======================

This code challenge reads in a JSON file of bank data, and outputs planned allocations & sources for income and expense events, and discretionary spending. 

Table of Contents:
- Code structure, algorithms, questions, and considerations.

REQUIRES:
========

Python 2.7.10

SETUP:
=====

1. run 'python even.py complex.input.json' on command line


TESTING:
=======

unittests.py asserts overall output plans correctly. 

PROCESS:
========

Understanding the problem well was a challenge. I started off working through the step-wise averaging algorithm (to calculate spendable values) on paper, and quickly wrote and tested the algorithm with lists of ints. 

I then created a model for the input data, and built a timeline of income & expense events. When testing out the step-wise averaging algorithm on events, I noticed that uneven time periods between income events led to many disproportionate spending values per day.

	My first instinct was to create sub-lists within my events list, chunked by income event. So, whenever a user would receive money, they would also calculate an evened spendable value. While re-reading the ReadMe, I noticed that my chunking method should be by primary income rather than all incomes, to allocate for a stable discretionary spending on that schedule. 



CODE STRUCTURE:
==============


Solvency at first calculates the overall year's net, which should be positive. 
During allocations, insolvency is again examined if a bill is unable to be met by previous funds. 


EVEN ALGORITHM:
==============

QUESTIONS:
==========

FUTURE CONSIDERATIONS:
======================


#TODO: 

I can anticipate an issue with input JSON where expenses are above incomes. My timeline currently does not do a secondary sort to place same-day income events before expense events, which is not necessary when income data is placed into a timeline before expense data. If the inputs were reversed, I would need to either edit the timeline construction to check for incomes to place before expenses, or implement a secondary sort of same-day events.


Because spending values are evened over the course of a timeline, it would be nice to know how much money you are displacing to a future month (or more specifically, income period). Since for each transaction, allocations + spendings != income amounts, this could be fixed by adding an allocation for "spending money to be used next time". 


My timeline currently expects very specific input data based on patterns I noticed in complex.input.json. I would need to update my model to handle schedules that vary further. 


I need to handle money calculations more accurately. I didn't know what the standard approach to dealing with monetary calculations was, but I assumed there would be some wrapper I would use in practice that handles cents, different currencies, etc. Here, I'm just doing regular calculations and casting final values to Decimal rounded-half-up two places. This is likely not best practice.













