import os, extraction, prediction, scraping, creation
import pandas as pd
from set_up.league_data import seasons
from job.work import reportage

import logging

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
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
        dataframe = pd.concat([dataframe, df])

    next = pd.read_csv(f"data/leagues/next.csv", index_col=0)
    return dataframe, next


def magic_flow():
    validate_datafolder(seasons)
    df, Xnot = get_data(seasons)
    df, Xnot = creation.create_dataset(df, Xnot)
    predictions = prediction.predict_scores(df, Xnot)
    reportage.report(predictions)


if __name__ == "__main__":
    magic_flow()
