# # US House Prices and Recessions # #
#
#
# Are house prices in university towns in the US less affected during recessions than non-university towns?
#
# This project uses three data files collected from the internet: 
# 
# 1) university_towns.txt - a text file of US college towns copied from Wikipedia
# 2) gdplev.xls - GDP over time of the United States in current dollars
# 3) City_Zhvi_AllHomes.csv - housing data for the US
#
# Goal: Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the # recession starts compared to the recession bottom.
#
# Import libraries to use:
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import uni_functions as uf
import os
os.system('cls' if os.name == 'nt' else 'clear')

print('-------------------------------------')
print('This Python script determines whether house prices in university towns were affected more or less by the recession than house prices in non-university towns making use of the following three pieces of data:\n')
print( '* From the Zillow research data site - http://www.zillow.com/research/data/ - there is housing data for the United States. In particular the datafile for all homes at a city level - http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv - ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.\n')
print( '* From the Wikipedia page on college towns is a list of university towns in the United States - https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States - which has been copied and pasted into the file ```university_towns.txt```.\n')
print( '* From Bureau of Economic Analysis, US Department of Commerce, the GDP over time - http://www.bea.gov/national/index.htm#gdp - of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. We will only look at GDP data from the first quarter of 2000 onward.\n')


input("Press Enter to continue...\n")

print("First take a look at the data in 'university_towns.txt': \n")
print(pd.read_table('university_towns.txt', header = None, names = ['RegionName']))

input("\nNot too pretty.\nPressing Enter executes the function 'get_uni_towns()' from the module 'uni_functions.py' and returns a data frame with columns 'State' and 'RegionName'...\n")

university_towns = uf.get_uni_towns()

print(university_towns)

print("\n...which looks much better.\n\nNow for the GDP information.\n")

input("Press Enter to see the data from the file 'gdplev.xls' in raw form\n")

print(pd.read_excel('gdplev.xls'))

print("\nNot too pretty either...\n") 

input("Pressing Enter calls the function 'gdp_tidy()' from 'uni_functions.py' clears things up considerably...")

gdp = uf.gdp_tidy()

print(gdp)

print("\n...leaving us with the GDP per quarter in chained 2009 USD since 2000.")

input("\nNow for the house price data for homes in the US at city level. The raw data from `City_Zhvi_AllHomes.csv' looks like this:\n")

print(pd.read_csv('City_Zhvi_AllHomes.csv'))

print("\n...again this is a mess - the data is monthly and the state names are abbreviated.\n")

input("Pressing Enter calls the function 'housing_data_quarters()' from 'uni_functions.py', which returns a data frame of the average house price in each city per quarter from January 2000 onwards...\n")

house_prices = uf.housing_data_quarters()

print(house_prices)

print("\nWith our datasets all clean and tidy it's time to find out when the recession began, when it ended, and how bad it got.\n")

input("\nPressing Enter calls the function 'get_recession_start()' from 'uni_functions.py', which returns the first of two consecutive quarters in which the GDP decreased.\n")

print(uf.get_recession_start())

input("\nPressing Enter calls the function 'get_recession_end()' from 'uni_functions.py', which returns the last of two consecutive quarters in which the GDP increased, signalling the end of the recession.\n")

print(uf.get_recession_end())

input("\nPressing Enter calls the function 'get_recession_bottom()' from 'uni_functions.py', which returns the quarter with lowest GDP during the recession.\n")

print(uf.get_recession_bottom())

print("\nThe recession therefore began in " + uf.get_recession_start() + ", ended in " + uf.get_recession_end() + ", and GDP was lowest in " + uf.get_recession_bottom() + '.\n')

print("\nWe separate the housing prices data frame into two, one for university towns, one for non-university towns.\n")

input("Pressing Enter calls 'get_uni_town_prices()' and 'get_non_uni_town_prices()' from 'uni_functions.py' in order to separate the dataframe...")

print("\nUniversity towns:\n")

uni_prices = uf.get_uni_town_prices()

print(uni_prices)

print("\nNon-university towns:\n")

non_uni_prices = uf.get_non_uni_town_prices()

print(non_uni_prices)

print("\nCreate a new column in each of these dataframes, called 'Price Ratio', with entries given by\n\n(house price in quarter before recession began) / (house price in quarter of recession with lowest GDP).")

input("\nPressing Enter calls get_price_ratio()' from 'uni_functions.py' first with university town prices, then with non-university town prices.\n")

print("\nUniversity towns:\n")

uni_ratio = uf.get_price_ratio(uni_prices)

print(uni_ratio)

print("\nNon-university towns:\n")

non_uni_ratio = uf.get_price_ratio(non_uni_prices)

print(non_uni_ratio)

print("Let's compare the ratio between the two groups, to see whether there is a significant overall difference between the price ratios for university and non-university towns.")

print("\nThe non-university towns have an average price ratio of: \n")
print(non_uni_ratio.mean())
print("\nwith standard deviation:\n")
print(non_uni_ratio.std())
print("\nWhile the university towns have an average price ratio of:\n")
print(uni_ratio.mean())
print("\nwith standard deviation:\n")
print(uni_ratio.std())

input("\nPressing Enter will run a t-test on the two sets of price ratios, by calling ttest_ind(a,b) from the package scipy.stats, where a is the set of price ratios for university towns and b the price ratios for non-university towns.\n")

print("Result of t-test:\n")

result = ttest_ind(non_uni_ratio,uni_ratio)

print(result)

p_val = result[1]

different = p_val < 0.01

print("\nThe p-value is:\n")

print(p_val)

print("\nTherefore the null hypothesis, that the price ratios are not significantly different, is "+ str(~different))













