from __future__ import division, print_function
import datetime as dt
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from calendar import monthrange
import solvency
import timeline

#Even Algorithm Module.
#Requires: Input Array of Events (from timeline)
#Modifies: Input Array of Events
#Effects: Groups subarrays of Events based on payday into Paychunk objects. Calculates evened_spending.

# 1 - chunk timeline by primary income source dates