
EVEN FINANCIAL PLANNER
======================

This financial planner reads in a JSON file of bank data, and outputs planned allocations & sources for income and expense events, and discretionary spending. 

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

I started off working through the step-wise averaging algorithm (to calculate spendable values) on paper, and quickly wrote and tested the algorithm with lists of ints. 

I then created a model for the input data, and built a timeline of income & expense events. When testing out the step-wise averaging algorithm on events, I noticed that uneven time periods between income events led to many disproportionate spending values per day. So, I updated the step-wise averaging to account for days. (The step-wise averaging algorithm in my code is: allocations.flow_money())

	On the first try accounting for days, I was taking the net values per income event, dividing that by the number of days to find the initial rate, and then while averaging, I was dividing the sum of the total rates by the number of chunks I was averaging. It took some testing for me to notice that these numbers weren't calculated accurately. 

		Example: 
		** Try averaging 3 income events to calculate evened_spending values:
		** numerators = net values (after provisioning for bills)
		** denominators = number of days until next income

		First try:
		(x/a + y/b + z/c) != (x+y+z)/3.

		Second, correct try:
		(x/a + y/b + z/c)  ==  [(x/a)*a + (y/b)*b + (z/c)*c] / [a+b+c].


My decisions on tackling the problem were two-fold:
	1 - First, provision bills and create the allocations / sources.

		I did this using two lists, to hold primary and secondary income sources. Then, I iterated through events sequentially and allocated the *most recent* income source (secondary before primary) to expenses.

		By the end of the allocations, I had a remaining list of primary and secondary income sources with money left over a the earliest dates after provisioning for bills. 

	2 - Second, use the remainder of primary and secondary income lists to even out spendable money 	based on the original step-wise averaging algorithm (above). 

		An assumption I held originally was that spending + allocations should equal income_amounts. 

		While this is a necessary assertion for the total, overall amounts (in unittests.py), it can only be true per income event if (net - spendable) were appended as an allocation to each income event, as "allocated for next month's spending money." I didn't see this in the README's output, so it's not in this program. My opinion is that adding that field would give a user clarity on where spending money is sourcing from/to.


		Solvency is calculated first for the overall year's net value, which should be positive. 
		During allocations, insolvency is again examined if a bill is unable to be met by previous funds. Example: (-400, -300, -200, +100000) means you're solvent overall, but insolvent for the first three bills. In my program, overall solvency is calculated initially, and expense-based solvency is calculated while allocating & provisioning for bills.


CODE STRUCTURE:
===============

even.py

	main() controls the flow of the program.

model.py

	get_transaction_data() creates a model of Transaction objects from input JSON.

timeline.py

	Timeline.create_timeline(transactions) uses Transaction objects with schedules to build a sorted by date timeline of Event objects.

allocations.py
	
	apply_allocations(timeline) runs through timeline's Events and appends sources & allocations for bills based on most recent income. Uses secondary incomes first, and primary incomes for any leftover expense. 


	calculate_spendings(tl, primary, secondary) controls the flow of spendable calculations.

		income_source_timelines(tl, primary, secondary) prepares the resulting primary and secondary income sources for calculating spendable values. It combines the two lists, sorts by date, and assigns 'net_days' and 'evened_rate' values, which are calculated using the left-over provisioned money per date. 

		flow_money(income_sources) calculates evened_spending money for each income source remaining from the provisioning, and reassign_spending(tl, income_sources) assigns new spending values to the corresponding event in timeline. 


unittests.py

	sound_income_allocations(tl) asserts that overall, allocations + spendings = incomes.



EVEN ALGORITHM:
==============

QUESTIONS:
==========

FUTURE CONSIDERATIONS:
======================


I can anticipate an issue with input JSON where expenses are above incomes. The timeline currently does not do a secondary sort to place same-day income events before expense events, which is not necessary when income data is placed into a timeline before expense data. If the inputs were reversed, I would need to either edit the timeline construction to check for incomes to place before expenses, or implement a secondary sort of same-day events.


Because spending values are evened over the course of a timeline, it would be nice for a user to know how much money you are displacing to a future month (or more specifically, income period). Since for each transaction, allocations + spendings != income amounts, this could be fixed by adding an allocation for "spending money to be used next time". 


The built timeline currently expects very specific input data based on patterns I noticed in complex.input.json. I would need to update my model to handle schedules that vary further. 


I need to handle money calculations more accurately. I didn't know what the standard approach to dealing with monetary calculations was, but I assume there would be some wrapper I would use in practice that handles cents, different currencies, etc. Here, I'm just doing regular calculations and casting final values to Decimal rounded-half-up two places. This is likely not best practice.


Naming conventions should be consistent, and would certainly be addressed using a linter and code reviews.


NOTES:
=====


I have hardcoded the start and end dates into the Timeline class. For input data that ends significantly earlier than the end date, the last spending value will be massive as it will account for all of the remaining days until the end of the year. 






