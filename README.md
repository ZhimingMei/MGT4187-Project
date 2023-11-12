# MGT4187-Project
Project repository of the course MGT4187 in CUHK(SZ)

## Variable Description
| Variable Name                    | Data Type   | Description |
|:---------------------------------|:------------|:------------|
| imdb_id                          | object      | The unique identifier for the show or movie on IMDb. |
| title                            | object      | The title of the show or movie. |
| plot                             | object      | A brief description or synopsis of the show or movie. |
| type                             | object      | The type of content, e.g., movie, series, or episode. |
| rated                            | object      | The content rating of the show or movie (e.g., PG, G). |
| year                             | object      | The release year of the show or movie. |
| released_at                      | object      | The actual release date of the show or movie. |
| added_at                         | object      | The date when the show or movie was added to the platform. |
| runtime                          | object      | The duration of the show or movie, typically in minutes. |
| genre                            | object      | The genre(s) of the show or movie. |
| director                         | object      | The director(s) of the movie or show. |
| writer                           | object      | The writer(s) or screenplay author(s) of the movie or show. |
| actors                           | object      | The main cast or actors featured in the movie or show. |
| language                         | object      | The primary language(s) spoken in the movie or show. |
| country                          | object      | The country or countries where the movie or show was produced. |
| awards                           | object      | Awards won or nominations received by the movie or show. |
| metascore                        | float64     | The Metacritic score of the movie or show. |
| imdb_rating                      | float64     | The IMDb rating of the movie or show. |
| imdb_votes                       | object      | The number of votes a movie or show has received on IMDb. |
| production_budget                | float64     | The budget allocated for the production of the movie or show. |
| domestic_gross                   | float64     | The domestic gross revenue earned by the movie or show. |
| worldwide_gross                  | float64     | The worldwide gross revenue earned by the movie or show. |
| distributor                      | object      | The distribution company responsible for releasing the movie or show. |
| mpaa_rating                      | object      | The Motion Picture Association of America rating for the movie. |
| matched_profit_indicator         | int64       | Indicator if the movie or show matched a certain profit entry. |
| Network                          | object      | The television network or streaming service where the show is aired. |
| Critic Score                     | object      | The aggregated score of the movie or show from various critics. |
| Audience Score                   | object      | The aggregated score of the movie or show from the audience. |
| tv_link                          | object      | A link to more information about the TV show or series. |
| nob_audience                     | float64     | The number of audience reviews or ratings for the movie or show. |
| Rating                           | object      | The overall rating given to the movie or show by the audience. |
| Review_audience                  | object      | Textual reviews provided by the audience. |
| nob_critics                      | float64     | The number of critic reviews or ratings for the movie or show. |
| Sentiment                        | object      | The overall sentiment (positive, negative, neutral) of the reviews. |
| Review_critics                   | object      | Textual reviews provided by critics. |
| matched_audience_indicator       | float64     | Indicator if the movie or show matched a certain audience review. |
| matched_critics_indicator        | float64     | Indicator if the movie or show matched a certain critics' review. |
| matched_all_review_indicator     | float64     | Indicator if the movie or show matched overall review review. |



## Data Overview
### Summary of Non-Numeric Statistics

1. **Type Distribution**:
   - Movies: 682 entries
   - Series: 197 entries
   - Episodes: 23 entries

2. **Ratings Distribution**:
   - G (General Audience): 207 entries
   - PG (Parental Guidance Suggested): 157 entries
   - TV-G (General Audience for TV): 132 entries

3. **Release Year Distribution**:
   - The dataset contains titles ranging from 1928 to 2020, including ongoing series.

### Summary of Numeric Statistics

| Statistic               | Runtime (minutes) | Production Budget ($) |
|-------------------------|-------------------|-----------------------|
| **Count (Runtime)**     | 846               | 127                   |
| **Mean**                | 68                | $62,915,330           |
| **Standard Deviation**  | 40                | $50,298,370           |
| **Minimum**             | 1                 | $858,000              |
| **25th Percentile**     | 30                | $20,000,000           |
| **Median (50th)**       | 80.5              | $45,000,000           |
| **75th Percentile**     | 96                | $97,500,000           |
| **Maximum**             | 181               | $170,000,000          |


## TO DO LIST
- [x] Exploratory Data Analysis
- [ ] Data supplement
    - we need to supplement the profit & production data...