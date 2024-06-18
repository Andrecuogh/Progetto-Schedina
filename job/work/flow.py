import os
import pandas as pd
from etl_config.log import logger
from etl_config.league_data import seasons
from etl_utils import extraction, prediction, scraping, creation, reportage

logger.info("Import completed\n")


def validate_datafolder(seasons: dict) -> None:
    """Check the validity of the folder of data"""
    logger.info("Start validation of input data")
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
    logger.info("End validation of input data\n")


def get_data(seasons: dict) -> dict[pd.DataFrame]:
    """Load data tables"""
    logger.info("Start ingestion of data")
    goals = matches = prev_enc = pd.DataFrame()
    for year in seasons.keys():
        year_df = pd.read_csv(f"data/leagues/{year}.csv", index_col=0)
        logging_rows = len(year_df.giornata.unique())
        logger.info(
            f"Dataframe for year {year} contains {len(year_df)/logging_rows} matches per {logging_rows} matchdays"
        )
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
    logger.info("End ingestion of data\n")
    return dataframe, accessories


def magic_flow(seasons: dict) -> None:
    """Pipeline of the flow: loading, transformation, prediction"""
    validate_datafolder(seasons)
    df, accessories = get_data(seasons)
    accessories["ranking"] = creation.view_ranking(df)
    df = creation.create_dataset(df)
    predictions = prediction.predict_scores(df)
    reportage.report(accessories, predictions)


if __name__ == "__main__":
    magic_flow(seasons)
