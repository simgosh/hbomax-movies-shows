import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px


credits = pd.read_csv("credits.csv")
titles = pd.read_csv("titles.csv")

print(credits.isnull().sum().sort_values())
print(titles.isnull().sum().sort_values())
print(credits.dtypes)
print(titles.dtypes)
print(titles[["imdb_id", "imdb_votes", "imdb_score", "tmdb_popularity", "tmdb_score"]])

titles["type"] = titles["type"].astype("category")
credits["role"] = credits["role"].astype("category")
print(titles["type"].dtypes)
print(credits["role"].dtypes)
print(credits.nunique())
print(titles.nunique())

titles[["imdb_votes", "imdb_score", "tmdb_popularity", "tmdb_score"]] = titles[["imdb_votes", "imdb_score", "tmdb_popularity", "tmdb_score"]].fillna(titles[["imdb_votes", "imdb_score", "tmdb_popularity", "tmdb_score"]].mode())
print(titles[["imdb_votes", "imdb_score", "tmdb_popularity", "tmdb_score"]].isnull().sum())

credits["character"] = credits["character"].fillna("Unknown")
print(credits["character"].tail())
merged = titles.merge(credits, on="id", how="left")
print(merged.head())

type_detail = merged.groupby(["type", "role"]).agg(avg_imdb = ("imdb_score", "mean")).round(2)
print(type_detail)

genre_detail = merged.groupby("genres").agg(avg_imdb = ("imdb_score", "mean"),
                                           tmdb_pop = ("tmdb_popularity", "mean")).round(2)
print(genre_detail.head())

#Movies are more than Tv shows 

merged["type"].value_counts().plot(kind="barh", color="pink")
plt.show()

#how many countries total that produced movie and show?

print(merged["production_countries"].unique().shape)

#"production_countries" returning empty rows or empty space so fill that space with Unknown using regex and then remove with "dropna"

merged["production_countries"] = merged["production_countries"].str.strip("[]")
merged["production_countries"] = merged["production_countries"].replace(r'^s*$', "Unknown", regex=True)
merged.dropna(subset=["production_countries"], inplace=True)
print(merged["production_countries"].tail())

#Top 20 countries that produced content some countries are collab with each other 
plt.subplots(figsize=(12,6))
merged["production_countries"].value_counts().nlargest(20).sort_values(ascending=True).plot(kind="barh", color="red")
plt.xlabel("Total Count")
plt.ylabel("Production Countries")
plt.title("Top 20 Countries which Produced Content")
plt.show()

#visulization for releaseyear which year is the most which tyoe

type = merged.groupby("type")["release_year"].value_counts().sort_values().unstack().fillna(0).T.reset_index()
type.rename(columns={"type":"index", "release_year":"Year", "MOVIE":"Movie", "SHOW":"TV Show"}, inplace=True)
print(type)

fig = px.scatter(type, x="Year", y=["Movie", "TV Show"], width=700, height=600)
fig.show()

#age certification with type

merged["age_certification"] = merged["age_certification"].fillna("Unknown")
print(merged["age_certification"].tail())
print(merged["age_certification"].value_counts())

plt.subplots(figsize=(15,6))
merged.groupby("age_certification")["type"].value_counts().dropna().sort_values(ascending=False).plot(kind="barh", color="green")
plt.title("Age Certification with Type")
plt.ylabel("Age Certification")
plt.legend()
plt.show()

#Top 20 movies/shows which got maximum imdb votes

max_imdb_votes = merged[["title", "imdb_votes", "type"]].sort_values("imdb_votes", ascending=False).drop_duplicates().reset_index(drop=True)[0:20].round(-4)
max_imdb_votes.rename(columns={"title":"Title", "imdb_votes":"IMDB Votes", "type":"Type"}, inplace=True)
print(max_imdb_votes)

#TOP 20 for only TV SHOW : 

tv_shows = merged[merged["type"] == "SHOW"]
max_imdb_tv = tv_shows[["imdb_votes", "title"]].sort_values("imdb_votes", ascending=False).drop_duplicates().reset_index(drop=True)[0:20]
max_imdb_tv.rename(columns={"imdb_votes" : "IMDB Votes for TV", "title":"Title"}, inplace=True)
print(max_imdb_tv)

#TOP 20 for only MOVIE :
movie = merged[merged["type"] == "MOVIE"] 
max_imdb_movie = movie[["imdb_votes", "title"]].sort_values("imdb_votes", ascending=True).drop_duplicates().reset_index(drop=True)[0:20]
max_imdb_movie.rename(columns={"imdb_votes" : "IMDB Votes for Movie", "title":"Title"}, inplace=True)
print(max_imdb_movie)


#Top 10 movies&shows which got max tmdb pop : 

popularity_tmdb = merged[["tmdb_popularity", "tmdb_score", "title", "type"]].sort_values("tmdb_popularity", ascending=False).drop_duplicates().reset_index(drop=True)[:11]
popularity_tmdb.rename(columns={"tmdb_popularity":"TMDB Popularity", "tmdb_score":"TMDB Score", "title":"Title", "type":"Type"}, inplace=True)
print(popularity_tmdb)


#Top 10 movie&shows for imdb score with age certification

imdb_score_title = merged[["release_year", "imdb_score", "title", "age_certification"]].sort_values("imdb_score", ascending=False).drop_duplicates().reset_index(drop=True)[0:11]
imdb_score_title.rename(columns={"release_year":"Release Year", "imdb_score":"IMDB Score", "title":"Title", "age_certification":"Age Certification"}, inplace=True)
print(imdb_score_title)




