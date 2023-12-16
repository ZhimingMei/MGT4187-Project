import os
import glob
import pandas as pd
import numpy as np


file_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/searching_index/results_supplement'
os.chdir(file_path)
file_ls = glob.glob('results_*')

df = pd.concat(pd.read_csv(file) for file in file_ls)


df['release_date'] = pd.to_datetime(df['release_date'])

df[['release_date']].describe()


df_runtime = df[['runtimeMinutes']].dropna()

df_runtime['runtimeMinutes'] = df_runtime['runtimeMinutes'].astype(int)
df_runtime[['runtimeMinutes']].describe()

df[['production_budget', 'domestic_gross', 'worldwide_gross', 'search_index']].describe()

cluster_data_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/results_folder/clustering'
os.chdir(cluster_data_path)
cluster = pd.read_excel('movie_with clusters.xlsx')

cluster.sample(5)

df = pd.merge(df, cluster[['movie', 'cluster']], on='movie', how='left')

print(df['cluster'].isnull().sum())

df = df.dropna(subset=['cluster'])

cluster_dummy = pd.get_dummies(df['cluster'].astype(str), drop_first=True, dtype=float)
cluster_dummy.columns = ['cluster_0', 'cluster_1']
df = pd.concat([df, cluster_dummy], axis=1)

df['release_date'] = pd.to_datetime(df['release_date'])
df['profit'] = df['worldwide_gross'] - df['production_budget']

# taking the log
min_profit = df['profit'].min()
offset = abs(min_profit) + 1

df['log_profit'] = np.log(df['profit'] + offset)

df['log_production_budget'] = np.log(df['production_budget']+1)

df['log_numVotes'] = np.log(df['numVotes']+1)
# drop null value
df = df.dropna(subset='search_index')
df = df.reset_index()
# same period movie metrics
def calculate_same_period_metrics_with_id(index, window=5):
    current_release_date = df.iloc[index]['release_date']
    start_date = current_release_date - pd.DateOffset(days=window)
    end_date = current_release_date + pd.DateOffset(days=window)
    same_period = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date) & (df.index != index)]
    
    if same_period.empty:
        return pd.Series([0, 0, 0, 0, '', 0], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id', 'same_period_search_index'])
    
    ## make some modification here (average first then log transformation)
    profit_avg = same_period['profit'].mean()
    log_profit = np.log(offset+profit_avg)
    avg_rating = same_period['averageRating'].mean()
    budget_avg = same_period['production_budget'].mean()
    log_budget = np.log(budget_avg+1)
    same_period_movie_id = ','.join(same_period['tconst'])
    avg_search_index = same_period['search_index'].mean()
    
    return pd.Series([1, log_profit, avg_rating, log_budget, same_period_movie_id, avg_search_index], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id', 'same_period_search_index'])

# Apply the updated function to each movie
df[['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id', 'same_period_search_index']] = df.index.to_series().apply(calculate_same_period_metrics_with_id)

import statsmodels.api as sm
from statsmodels.formula.api import ols

# Regression Model
model_formula = 'log_profit ~ log_production_budget+same_period_profit+same_period_rating+same_period_budget\
                +same_period_budget*same_period_profit\
                        +same_period_budget*same_period_search_index\
                            +same_period_budget*same_period_rating+\
                                same_period_profit*same_period_search_index+\
                                    same_period_profit*same_period_rating+\
                                        same_period_search_index*same_period_rating+\
                                            cluster_0+ cluster_1+\
                                                num_topics+averageRating'

results = ols(model_formula, data=df).fit()

# Conduct ANOVA analysis
anova_results = sm.stats.anova_lm(results, typ=2)