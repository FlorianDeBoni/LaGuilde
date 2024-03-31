import pandas as pd
from django.shortcuts import render
from ..models import *


def extract_data_as_dataframe(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Split the "Players" column into two columns
    df[['Player1', 'Player2']] = df['Players'].str.split('à', expand=True)

    # Drop the original "Players" column
    df.drop(columns=['Players'], inplace=True)

    return df


# Provide the path to your Excel file
file_path = r"c:\Users\flori\OneDrive\Documents\CS\2A\S8\Human Computer Interface\Project1\Boarding Games Rental\La_Guilde_Boarding_Games_Rental\La_Guilde_Boarding_Games_Rental\BGR\views\Inventaire.xlsx"

# Extract data from the Excel file into a DataFrame
data_dataframe = extract_data_as_dataframe(file_path)


def init_datas():
    for category in data_dataframe["Category"]:
        category = category.split(', ')
        for name in category:
            try:
                genre = Genre.objects.get(name=name)
            except:
                genre = Genre(name=name, name_en=name)
                genre.save()
    for index, row in data_dataframe.iterrows():
        try:
            name = row["Name"]
            player1 = int(row["Player1"])
            player2 = int(row["Player2"])
            time = row["Time"]
            quantity = row["Quantity"]
            categories = [Genre.objects.get(name=name)
                          for name in row["Category"].split(', ')]
            game = Game(name=name,
                        description_en="Description of "+name,
                        description_fr="Description de "+name,
                        quantity=quantity,
                        duration=time,
                        player_number_max=player2,
                        player_number_min=player1)
            game.save()
            for genre in categories:
                game.genre.add(genre)
        except:
            pass
