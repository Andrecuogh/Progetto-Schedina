import os
import pandas as pd
import logging
import logging.config
from etl_config.league_data import seasons
from etl_utils import extraction, prediction, scraping, creation, reportage
from etl_config.log import LOG_CONFIG


logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("etl_flow")
logger.info("Import completed")


def validate_datafolder(seasons: dict) -> None:
    """Check the validity of the folder of data"""
    for year in seasons.keys():
        logger.info(f"checking available data for year {year}...")
        is_file = os.path.isfile(f"data/leagues/{year}.csv")
        if not is_file or seasons[year]["days"] != 38:
            logger.info("Output: False. Downloading data from skysport.com")
            scraping.scrape_sky(
                year=year, ongoing=seasons[year]["ongoing"], days=seasons[year]["days"]
            )
        else:
            logger.info("Output: True")


def get_data(seasons: dict) -> dict[pd.DataFrame]:
    """Load data tables"""
    goals = matches = prev_enc = pd.DataFrame()
    for year in seasons.keys():
        year_df = pd.read_csv(f"data/leagues/{year}.csv", index_col=0)
        goal, match = extraction.extract_features(year_df)
        goals = pd.concat([goals, goal])
        matches = pd.concat([matches, match])
        prev_enc = pd.concat([prev_enc, year_df])

    prev_enc = creation.transform_previous_encounters(prev_enc)

    dataframe = {
        "goals": goals,
        "matches": matches,
    }
    accessories = {
        "previous_encounters": prev_enc,
    }
    return dataframe, accessories


def magic_flow(seasons: dict) -> None:
    """Pipeline of the flow: loading, transformation, prediction"""
    validate_datafolder(seasons)
    df, accessories = get_data(seasons)
    df = creation.create_dataset(df)
    predictions = prediction.predict_scores(df)
    reportage.report(accessories, predictions)


if __name__ == "__main__":
    magic_flow(seasons)
