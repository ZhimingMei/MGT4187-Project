# MGT4187-Project
Project repository of the course MGT4187 in CUHK(SZ). This repo has been archived.

## Variable Description

| Column Name         | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `tconst`            | Unique identifier for each title in the dataset.             |
| `titleType`         | The type of title (e.g., movie, short, TV series).           |
| `primaryTitle`      | The main title of the work.                                  |
| `originalTitle`     | The original title of the work in its original language.     |
| `isAdult`           | Indicates whether the title is adult content (boolean).      |
| `startYear`         | The year when the title was released or started.             |
| `endYear`           | The year when the title ended (applicable for TV series).    |
| `runtimeMinutes`    | Duration of the title in minutes.                            |
| `genres`            | Genres associated with the title.                            |
| `title_std`         | Standardized version of the title name.                      |
| `release_date`      | The release date of the title.                               |
| `movie`             | Indicates if the title is a movie (boolean).                 |
| `production_budget` | Budget allocated for the production of the title.            |
| `domestic_gross`    | Gross revenue in the domestic market.                        |
| `worldwide_gross`   | Total gross revenue worldwide.                               |
| `distributor`       | Company distributing the title.                              |
| `mpaa_rating`       | MPAA rating of the title.                                    |
| `genre`             | Primary genre of the title.                                  |
| `movie_same_name`   | Indicator equals to 1 if the title from profit data is the same as that from ratings data |
| `averageRating`     | The average rating of the title.                             |
| `numVotes`          | Number of votes the title has received.                      |



## TO DO LIST

All finished!

## Reference

### Data source

1. IMDB ratings data: [IMDB non commercial datasets](https://developer.imdb.com/non-commercial-datasets/)
2. Budget and profit data: [the-numbers.com](https://www.the-numbers.com/)
3. Review data: [Rotten Tomatoes Reviews for Online Streaming Shows](https://www.kaggle.com/datasets/coltonbarger/rotten-tomatoes-reviews-for-online-streaming-shows)