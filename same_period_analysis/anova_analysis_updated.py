import glob
import os
import math

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.preprocessing import MinMaxScaler

file_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/searching_index/results_supplement'
os.chdir(file_path)
file_ls = glob.glob('results_*')

df = pd.concat(pd.read_csv(file) for file in file_ls)

df['release_date'] = pd.to_datetime(df['release_date'])
df['profit'] = df['worldwide_gross'] - df['production_budget']

# min_profit = df['profit'].min()
# offset = abs(min_profit) + 1

# df['log_profit'] = np.log(df['profit'] + offset)

# df['log_production_budget'] = np.log(df['production_budget']+1)
# dropna based on searching index
df = df.dropna(subset='search_index')
final_data_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/results_folder/data_cleaning_result'

os.chdir(final_data_path)
df.to_csv('final_data.csv')

df = df.reset_index()
# same period movie metrics
def calculate_same_period_metrics_with_id(index, window=10):
    current_release_date = df.iloc[index]['release_date']
    start_date = current_release_date - pd.DateOffset(days=window)
    end_date = current_release_date + pd.DateOffset(days=window)
    same_period = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date) & (df.index != index)]
    
    if same_period.empty:
        return pd.Series([0, 0, 0, 0, '', 0], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id', 'same_period_search_index'])
    
    avg_profit = same_period['profit'].mean()
    avg_rating = same_period['averageRating'].mean()
    avg_budget = same_period['production_budget'].mean()
    same_period_movie_id = ','.join(same_period['tconst'])
    avg_search_index = same_period['search_index'].mean() if 'search_index' in same_period else 0
    
    return pd.Series([1, avg_profit, avg_rating, avg_budget, same_period_movie_id, avg_search_index], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id', 'same_period_search_index'])

# Apply the updated function to each movie
df[['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id', 'avg_search_index']] = df.index.to_series().apply(calculate_same_period_metrics_with_id)
#### Filter the sample based on Ratings
# filtered_df = df.loc[df['averageRating']>7]

# Regression Model
model_formula = 'profit ~ same_period_indicator * same_period_profit + same_period_indicator * same_period_rating + same_period_indicator * same_period_budget+ same_period_indicator* avg_search_index'
model = ols(model_formula, data=df).fit()

# Conduct ANOVA analysis
anova_results = sm.stats.anova_lm(model, typ=2)

# ANOVA summary & Regression summary
anova_results, model.summary()



#### new model: including the high-rating dummy
# df['high_rating_dummy'] = (df['averageRating'] > 7).astype(int)

# model_formula = 'profit ~ production_budget + same_period_profit + same_period_budget + high_rating_dummy + high_rating_dummy:same_period_profit + high_rating_dummy:same_period_budget'
# model = ols(model_formula, data=df).fit()
# print(model.summary())


# model_formula = """
# profit ~ production_budget + 
#          same_period_indicator + 
#          same_period_profit + 
#          same_period_budget + 
#          high_rating_dummy + 
#          high_rating_dummy:same_period_indicator + 
#          high_rating_dummy:same_period_profit + 
#          high_rating_dummy:same_period_budget
# """
# model = ols(model_formula, data=df).fit()
# print(model.summary())