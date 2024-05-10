import os, sys

sys.path.append(os.getcwd().replace("\\", "/").replace("/job/work", ""))

import extraction, prediction, scraping, creation
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
    goals = matches = pd.DataFrame()
    for year in seasons.keys():
        year_df = pd.read_csv(f"data/leagues/{year}.csv", index_col=0)
        goal, match = extraction.extract_features(year_df)
        goals = pd.concat([goals, goal])
        matches = pd.concat([matches, match])

    dataframe = {"goals": goals, "matches": matches}
    return dataframe


def magic_flow():
    validate_datafolder(seasons)
    df = get_data(seasons)
    df = creation.create_dataset(df)
    predictions = prediction.predict_scores(df)
    reportage.report(predictions)


if __name__ == "__main__":
    for day in range(5, 6):
        seasons["2023"]["days"] = day
        magic_flow()
