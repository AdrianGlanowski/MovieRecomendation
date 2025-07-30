import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt


def filter_movies_based_on_genres(df, set_of_genres):
    return df[df["genres"].apply(lambda genres: set(genres.split("|")).issuperset(set_of_genres))]


def plot_how_many_of_each_review(merged):
    merged.drop(columns=["genres", "title"]).groupby(["rating"]).count().rename(columns={"movieId": "count"}).plot()
    plt.show()


def main():

    movies = pd.read_csv("assets\\movies.csv")
    ratings = pd.read_csv("assets\\ratings.csv").drop(columns=["userId", "timestamp"]).groupby(["movieId"]).mean().round(1)
   
    tags = pd.read_csv("assets\\tags.csv").drop(columns=["userId", "timestamp"])
    tags["tag"] = tags.groupby(["movieId"]).transform(lambda x: "|".join(x)).drop_duplicates()
    tags = tags[tags["tag"].notna()]
   
    merged = pd.merge(movies, ratings, how="left", on="movieId").merge(tags, how="left", on="movieId")

    genres = [
        'Adventure',
        'Animation',
        'Children',
        'Comedy',
        'Fantasy',
        'Romance',
        'Drama',
        'Action',
        'Crime',
        'Thriller',
        'Horror',
        'Mystery',
        'Sci-Fi',
        'War',
        'Musical',
        'Documentary',
        'IMAX',
        'Western',
        'Film-Noir']

    def compute(event=None):
        res = filter_movies_based_on_genres(movies, {genres[i] for i in range(len(chosen_genres)) if chosen_genres[i].get() == 1})["title"]
        res_frame = tk.Frame(root)
        for i in range(10):
            print(res.iloc[[i]])
        for i in range(10):
            tk.Label(res_frame, text=res.iloc[i])
        res_frame.tkraise()
    
    root = tk.Tk()
    root.title("Movie Recomendation")
    root.minsize(360, 200)

    chosen_genres=[tk.IntVar() for _ in range(len(genres))]

    frm = tk.Frame(root)
    frm.grid()
    for i, genre in enumerate(genres):
        tk.Label(frm, text=f"{genre}").grid(column=0, row=i)
        tk.Checkbutton(frm, variable=chosen_genres[i]).grid(column=1, row=i)
    
    tk.Button(frm, text="Search", command=compute).grid(column=1, row=len(genres))
    root.bind('<Return>', compute)
    root.mainloop()

main()