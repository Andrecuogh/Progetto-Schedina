import os
import pandas as pd
from league_data import seasons
from etl_utils import extraction, prediction, scraping, creation, reportage


import logging

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
logging.info("Import completed")


def validate_datafolder(seasons: dict) -> None:
    """Check the validity of the folder of data"""
    for year in seasons.keys():
        is_file = os.path.isfile(f"data/leagues/{year}.csv")
        if not is_file or seasons[year]["ongoing"]:
            scraping.scrape_sky(
                year=year, ongoing=seasons[year]["ongoing"], days=seasons[year]["days"]
            )


def get_data(seasons: dict) -> dict[pd.DataFrame]:
    """Load data tables"""
    goals = matches = pd.DataFrame()
    for year in seasons.keys():
        year_df = pd.read_csv(f"data/leagues/{year}.csv", index_col=0)
        goal, match = extraction.extract_features(year_df)
        goals = pd.concat([goals, goal])
        matches = pd.concat([matches, match])

    next = goals.sort_values(by=["anno", "giornata"]).iloc[-20:]
    next.to_csv("data/leagues/next.csv", index=False)

    dataframe = {"goals": goals, "matches": matches}
    return dataframe


def magic_flow(seasons: dict) -> None:
    """Pipeline of the flow: loading, transformation, prediction"""
    validate_datafolder(seasons)
    df = get_data(seasons)
    df = creation.create_dataset(df)
    predictions = prediction.predict_scores(df)
    reportage.report(predictions)


if __name__ == "__main__":
    magic_flow(seasons)
