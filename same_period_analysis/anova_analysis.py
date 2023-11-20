import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols


file_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/data/final_data/filtered_data_w_ratings.csv'
df = pd.read_csv(file_path)
df['release_date'] = pd.to_datetime(df['release_date'])
df['profit'] = df['worldwide_gross'] - df['production_budget']

# same period movie metrics
def calculate_same_period_metrics_with_id(index, window=5):  # 5 days before and after
    current_release_date = df.iloc[index]['release_date']
    start_date = current_release_date - pd.DateOffset(days=window)
    end_date = current_release_date + pd.DateOffset(days=window)
    same_period = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date) & (df.index != index)]
    
    if same_period.empty:
        return pd.Series([0, 0, 0, 0, ''], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id'])
    
    sum_profit = same_period['profit'].sum()
    avg_rating = same_period['averageRating'].mean()
    sum_budget = same_period['production_budget'].sum()
    same_period_movie_id = ','.join(same_period['tconst'])
    
    return pd.Series([1, sum_profit, avg_rating, sum_budget, same_period_movie_id], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id'])


df[['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id']] = df.index.to_series().apply(calculate_same_period_metrics_with_id)

#### Filter the sample based on Ratings
# filtered_df = df.loc[df['averageRating']>7]

# Regression Model
model_formula = 'profit ~ same_period_indicator * same_period_profit + same_period_indicator * same_period_rating + same_period_indicator * same_period_budget'
model = ols(model_formula, data=df).fit()

# Conduct ANOVA analysis
anova_results = sm.stats.anova_lm(model, typ=2)

# ANOVA summary & Regression summary
anova_results, model.summary()
