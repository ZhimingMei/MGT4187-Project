import pandas as pd
import os

data_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/data'

os.chdir(data_path)
profit = pd.read_csv('movie_profit.csv', index_col=0)

print(profit.columns)

# check the nan value in production budget col
print('nan value in production budget: ', profit['production_budget'].isna().sum())

disney_plus = pd.read_csv('disney_plus_shows.csv')

print(disney_plus.columns)

profit.rename(columns={'movie': 'title'}, inplace=True)

disney_plus = pd.merge(disney_plus, profit[['title', 'production_budget', 'domestic_gross', 'worldwide_gross', 'distributor', 'mpaa_rating']], on='title', how='left')

# check the matched pairs
disney_plus['matched_profit_indicator'] = disney_plus['production_budget'].notnull().astype(int)
print(f'the original length: {disney_plus.__len__()}; the matched pairs: {disney_plus.matched_profit_indicator.sum()}')


review_path = '/Users/ryan/Documents/GitHub/MGT4187-Project/data/review_data'
os.chdir(review_path)

audience = pd.read_csv('audience_reviews.csv')
print(audience.columns)
print(f'total length of audience review data: {audience.__len__()}; unique show: {audience.Show.unique().__len__()}')


critic = pd.read_csv('critic_reviews.csv')
print(critic.columns)
print(f'total length of critic data: {critic.__len__()}; unique show: {critic.Show.unique().__len__()}')

tv_show = pd.read_csv('tv_show_links.csv')
print(tv_show.columns)
print(f'total length of tv_show data: {tv_show.__len__()}')

# grouping the review data first

## audience data
grouped_audience = audience.groupby('Show', dropna=False)

agg_audience_nob = pd.DataFrame({
        'nob_audience': grouped_audience.size()
}).reset_index()

agg_audience = grouped_audience.agg({
    'Rating': lambda x: list(pd.unique(x)), 
    'Review': lambda x: list(pd.unique(x))
})

audience_data = pd.merge(agg_audience_nob, agg_audience, on='Show')
print(audience_data.sample(5))

## critics data
grouped_critics = critic.groupby('Show', dropna=False)

agg_critics_nob = pd.DataFrame({
        'nob_critics': grouped_critics.size()
}).reset_index()
agg_critics = grouped_critics.agg({
    'Sentiment': lambda x: list(pd.unique(x)), 
    'Review': lambda x: list(pd.unique(x))
})

critics_data = pd.merge(agg_critics_nob, agg_critics, on='Show')
print(critics_data.sample(5))

## finalized check
audience_data.rename(columns={'Review': 'Review_audience'}, inplace=True)
tv_show = pd.merge(tv_show, audience_data, on='Show', how='left')

critics_data.rename(columns={'Review': 'Review_critics'}, inplace=True)
tv_show = pd.merge(tv_show, critics_data, on='Show', how='left')


tv_show['matched_audience_indicator'] = tv_show['Review_audience'].notnull().astype(int)
tv_show['matched_critics_indicator'] = tv_show['Review_critics'].notnull().astype(int)

print(f'the matched pairs from audience review: {tv_show.matched_audience_indicator.sum()}')
print(f'the matched pairs from critics: {tv_show.matched_critics_indicator.sum()}')

tv_show['matched_all_review_indicator'] = (tv_show['matched_audience_indicator'] & tv_show['matched_critics_indicator']).astype(int)
print(f'the matched results from all review data: {tv_show.matched_all_review_indicator.sum()}')

## finalized data
tv_show.rename(columns={'Show': 'title'}, inplace=True)
disney_plus = pd.merge(disney_plus, tv_show, on='title', how='left')

print(disney_plus.sample(5))
