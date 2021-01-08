import yfinance as yf
import pandas as pd
import matplotlib as mpl
import csv
import numpy as np
import matplotlib.pyplot as plt

stock =  input("What stock would you like to anaylize?\n")

print ("Analysing Stock")

Ticker = yf.Ticker(stock)

print (Ticker.institutional_holders)
print (Ticker.major_holders)

Hist = Ticker.history(period="5y")

print(Hist)

# Data
df = pd.DataFrame(Ticker.history(period="5y"))

# Calculate % Change column
close_minus_open = (df['Close'] - df['Open'])/df['Open']*100

days_in_a_row = []

for day in range(len(close_minus_open)):
  # If this is the first day in the df
  if day == 0:
    # Appending positive is mooning, negative is down trend
    # If down trend
    if close_minus_open[day] < 0:
      days_in_a_row.append(-1)
    elif close_minus_open[day] > 0:
      days_in_a_row.append(1)
  else:
    # Current streak is last index
    current_streak = days_in_a_row[-1]
    today_was_green = True if close_minus_open[day] > 0 else False

    if today_was_green and current_streak > 0:
      # Continuous uptrend
      days_in_a_row.append(current_streak+1)
    elif today_was_green and current_streak < 0:
      # Broke downtrend, new uptrend
      days_in_a_row.append(1)
    elif not today_was_green and current_streak > 0:
      # Broke uptrend, new downtrend
      days_in_a_row.append(-1)
    elif not today_was_green and current_streak < 0:
      # Continuous, downtrend
      days_in_a_row.append(current_streak - 1)

Hist['Percent Change'] = close_minus_open
Hist['Day Trend'] = days_in_a_row
print(Hist)
