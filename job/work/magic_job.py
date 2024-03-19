import os, extraction, creation, prediction, scraping
import pandas as pd
from set_up.league_data import seasons
from predict import reportage
import logging

logging.info("Import completed")


def validate_datafolder(seasons):
    for year in seasons.keys():
        is_file = os.path.isfile(f"data/leagues/{year}.csv")
        if not is_file or seasons[year]["ongoing"]:
            scraping.scrape_sky(
                year=year, ongoing=seasons[year]["ongoing"], days=seasons[year]["days"]
            )


def get_data(seasons):
    dataframe = pd.DataFrame()
    for year in seasons.keys():
        year_df = pd.read_csv(f"data/leagues/{year}.csv", index_col=0)
        df = extraction.extract_features(year_df)
        pd.concat([dataframe, df])
    return dataframe


def predict():
    pass


def magic_flow(day):
    validate_datafolder(seasons)
    df = get_data(seasons)
    Xnot = creation.create_matchday_df(list_ls[-1], lat_day)

    predictions = [prediction.predict_scores(df, target, Xnot) for target in targets]

    reportage.save_report(predictions)
    reportage.display_report(predictions)


if __name__ == "main":
    magic_flow()
