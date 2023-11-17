# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 2023

@author: zhiming
"""

import time
import pandas as pd
import os

from pytrends.request import TrendReq
from datetime import datetime, timedelta


def fetch_trend(movie_title, release_date):
    # calculate the start date
    start_date = release_date - timedelta(days=365)

    # change the datetime format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = release_date.strftime('%Y-%m-%d')

    # build the payload
    pytrends.build_payload(kw_list=[movie_title], timeframe=f'{start_date_str} {end_date_str}')

    # fetch the interest over time
    trends = pytrends.interest_over_time()

    # return the mean (we can change mean to other statistics)
    return trends[movie_title].mean()


#### main program
if __name__ == '__main__':
    ## read data
    input_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/data/final_data'

    os.chdir(input_path)
    data = pd.read_csv('filtered_data_w_ratings.csv')

    ## settings
    pytrends = TrendReq(hl='en-US', tz=360)



    data_sample = data.sample(5) # comment this line, and check your input again before running the program

    for index, row in data_sample.iterrows():
        # convert to datetime object
        release_date = pd.to_datetime(row['release_date'])

        # retrieve the data
        trend_index = fetch_trend(row['primaryTitle'], release_date)

        # store the data
        data_sample.at[index, 'search_index'] = trend_index

        # to avoid the error that reach the maximum retrieve matrix
        time.sleep(20)