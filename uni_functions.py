# Library of functions to compare university town house prices during recession
import pandas as pd
import numpy as np
import scipy.stats as ttest_ind
import matplotlib.pyplot as plt

######################################################

def get_uni_towns():
	# Function that cleans and tidies data from 'university_towns.txt', returning a dataframe with columns 'State' and 'RegionName'
	# Import txt file:
	uni_towns = pd.read_table('university_towns.txt', header = None, names = ['RegionName'])

	# Create a column ('is_state') of boolean values with entry 'True' if line contains '[edit]' and 'False' otherwise

	uni_towns['is_state'] = uni_towns['RegionName'].str.contains(r'\[edit\]')

	# Create a column 'state_num' that sums the entries of 'is_state', where True = 1, False = 0

	uni_towns['state_num'] = uni_towns['is_state'].cumsum()

	# Create a column 'reg_num' which counts the regions within each state

	uni_towns['reg_num'] = uni_towns.groupby('state_num').cumcount()

	# Create a column of states corresponding to towns

	uni_towns['State'] = uni_towns.groupby('state_num')['RegionName'].transform('first')

	# Clean up state names

	uni_towns['State'] = uni_towns['State'].str.replace(r'\[edit\]' , '')

	# Clean up town names

	uni_towns['RegionName'] = uni_towns['RegionName'].str.replace(r' \(.+$' , '')

	# Remove towns that are actually states

	uni_towns = uni_towns.loc[~uni_towns['is_state']]

	# Remove everything except 'State' and 'RegionName' column

	return uni_towns[['State', 'RegionName']]

######################################################

def gdp_tidy():
		# Function finds quarter in which recession began (two consecutive quarters of negative GDP)

	# Import gdplev.xls file

	gdp = pd.read_excel('gdplev.xls').iloc[7:]

	# Only interested in chained GDP for quarters so take relevant columns

	gdp = gdp[['Unnamed: 4', 'Unnamed: 6']]

	# Rename the columns 

	gdp.columns = ['Quarters', 'GDP']

	# extract data from 2000 onwards

	return gdp[gdp['Quarters'].str.startswith('20')].reset_index(drop=True)

#######################################################

def get_recession_start():

	# Function finds quarter in which recession began (two consecutive quarters of negative GDP)

	# Calls tidy gdp dataframe

	gdp = gdp_tidy()

	# Create new column which contains difference between GDP of row x and GDP of row x+1

	gdp['Diff'] = gdp['GDP'].iloc[1:].copy().reset_index(drop=True) - gdp['GDP']

	# Restrict to those rows with negative difference

	gdp_neg = gdp[gdp['Diff']<0]

	for i in range(0, len(gdp_neg.index)-1):
		if gdp_neg.index[i] == gdp_neg.index[i+1]-1:
			rec_begin = i+1
			break

	return gdp_neg['Quarters'].iloc[rec_begin]

##########################################

def get_recession_end():

	# Finds quarter in which recession ended
	# Call tidy gdp

	gdp = gdp_tidy()


	# Index by quarters

	gdp = gdp.set_index('Quarters')

	gdp_recession = gdp.loc[get_recession_start():]

	gdp_recession = gdp_recession.reset_index()

	gdp_recession['Diff'] = gdp_recession['GDP'].iloc[1:].copy().reset_index(drop=True) - gdp_recession['GDP']

	gdp_recovery = gdp_recession[gdp_recession['Diff']>0]

	for i in range(0, len(gdp_recovery.index)-1):
		if gdp_recovery.index[i] == gdp_recovery.index[i+1]-1:
			rec_end = i+2
			break

	return gdp_recovery['Quarters'].iloc[rec_end]

######################################

def get_recession_bottom():
	# Finds quarter with lowest GDP during recession

	# Call tidy gdp

	gdp = gdp_tidy()

	# Index by quarters

	gdp = gdp.set_index('Quarters')

	gdp = gdp.loc[get_recession_start():get_recession_end()]

	gdp = gdp.reset_index()

	return gdp['Quarters'].iloc[gdp['GDP'].idxmin()]

######################################

def housing_data_quarters():

	states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

	city_lev = pd.read_csv('City_Zhvi_AllHomes.csv')

	city_lev = city_lev.replace({ 'State' : states }, regex=True)

	city_lev = city_lev.set_index(['State','RegionName']) 

	city_lev_transpose = city_lev.T.loc['2000-01':] 

	count = int(len(city_lev_transpose)/3)


	for i in range(0,count):
		col_label = str(2000+i//4)+'q'+str( (i%4) + 1)
		city_lev[col_label] = (city_lev_transpose.iloc[(3*i):(3*i+3)]
												 .mean()
												 .T)

	city_lev['2016q3'] = city_lev_transpose.iloc[-2:].mean().T

	return (city_lev.T
					.loc['2000q1':]
					.T)

######################################

def get_uni_town_prices():

	# Get city level housing prices

	city_lev = housing_data_quarters()

	# Get data for university towns 

	university_towns = get_uni_towns().set_index(['State','RegionName'])

	### Get index consisting of intersection between uni towns and GDP data

	uni_index = (university_towns
					.index
					.intersection(city_lev.index)
					.values
					.tolist()
					)

	return city_lev.loc[uni_index]

######################################

def get_non_uni_town_prices():

	city_lev = housing_data_quarters()

	uni_house_prices = get_uni_town_prices()

	non_uni_index = (city_lev
						.index
						.symmetric_difference(uni_house_prices.index)
						.values
						.tolist()
						)

	return city_lev.loc[non_uni_index]

######################################

def get_price_ratio(dataframe):
	
	dataframe['Price Ratio'] = dataframe[get_recession_start()] / dataframe[get_recession_bottom()]	
	return dataframe['Price Ratio'].dropna()

##################################











