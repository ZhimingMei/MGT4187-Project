import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols


file_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/data/final_data/filtered_data_w_ratings.csv'
df = pd.read_csv(file_path)
df['release_date'] = pd.to_datetime(df['release_date'])
df['profit'] = df['worldwide_gross'] - df['production_budget']

# taking the log
min_profit = df['profit'].min()
offset = abs(min_profit) + 1

df['log_profit'] = np.log(df['profit'] + offset)

df['log_production_budget'] = np.log(df['production_budget']+1)


# same period movie metrics
def calculate_same_period_metrics_with_id(index, window=5):  # 5 days before and after
    current_release_date = df.iloc[index]['release_date']
    start_date = current_release_date - pd.DateOffset(days=window)
    end_date = current_release_date + pd.DateOffset(days=window)
    same_period = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date) & (df.index != index)]
    
    if same_period.empty:
        return pd.Series([0, 0, 0, 0, ''], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id'])
    
    avg_profit = same_period['log_profit'].mean()
    avg_rating = same_period['averageRating'].mean()
    avg_budget = same_period['log_production_budget'].mean()
    same_period_movie_id = ','.join(same_period['tconst'])
    
    return pd.Series([1, avg_profit, avg_rating, avg_budget, same_period_movie_id], index=['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id'])


df[['same_period_indicator', 'same_period_profit', 'same_period_rating', 'same_period_budget', 'same_period_movie_id']] = df.index.to_series().apply(calculate_same_period_metrics_with_id)

#### Filter the sample based on Ratings
# filtered_df = df.loc[df['averageRating']>7]

# Regression Model
model_formula = 'log_profit ~ same_period_indicator * same_period_profit + same_period_indicator * same_period_rating + same_period_indicator * same_period_budget'
model = ols(model_formula, data=df).fit()

# Conduct ANOVA analysis
anova_results = sm.stats.anova_lm(model, typ=2)

# ANOVA summary & Regression summary
anova_results, model.summary()



#### new model: including the high-rating dummy
df['high_rating_dummy'] = (df['averageRating'] > 7).astype(int)

model_formula = 'profit ~ production_budget + same_period_profit + same_period_budget + high_rating_dummy + high_rating_dummy:same_period_profit + high_rating_dummy:same_period_budget'
model = ols(model_formula, data=df).fit()

anova_results = sm.stats.anova_lm(model, typ=2)
anova_results, model.summary()


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

anova_results = sm.stats.anova_lm(model, typ=2)
anova_results, model.summary()
