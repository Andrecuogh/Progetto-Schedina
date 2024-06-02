import pandas as pd
import webbrowser
import urllib
from set_up.config_var import VERSION, REPOPATH
from set_up.league_data import LATEST_YEAR, TARGETS


class GitConnectionError(Exception):
    """Raised when connection to project's online repo fails"""

    def __init__(self, link):
        self.message = f"Connection to \n\t{link}\n has failed"
        super().__init__(self.message)


class RepoConnector:
    """Class to connect with the project's online GitHub repository"""

    def __init__(self):
        self.git_url = "https://raw.githubusercontent.com"
        self.repopath = REPOPATH
        self.path = f"{self.git_url}/{self.repopath}/main"

    def close_connection_if_exception(method):
        def wrapper(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except:
                link = args[0]
                raise GitConnectionError(link)

        return wrapper


class Updater(RepoConnector):

    def __init__(self):
        super().__init__()
        self.curr_version = VERSION
        self.version_path = f"{self.path}/data/version/versions.csv"
        self.upd_link = f"{self.path}/data/version/latest.apk"
        self.line = "Nuovo aggiornamento disponibile."

    def search_update(self):
        """Search new updates and, if available, update the app"""
        need_to_update = self.check_update(self.version_path)
        if need_to_update:
            self.update_app()

    @RepoConnector.close_connection_if_exception
    def check_update(self, link):
        """Check the availability of new versions from
        the project's GitHub repository
        """
        versions = pd.read_csv(link)
        self.latest_version = versions[versions["Latest"]]["Version"].values[0]
        self.no_updated = self.latest_version > self.curr_version
        return self.no_updated

    def update_app(self):
        """Update the app at latest version"""
        webbrowser.open(self.upd_link)


class Loader(RepoConnector):
    """Load the dataframes from the project's GitHub repository"""

    def __init__(self):
        super().__init__()
        self.latest_year = LATEST_YEAR
        self.targets = TARGETS
        self.metadata_path = f"{self.path}/data/metadata.csv"
        self.dataframe_path = f"{self.path}/data/{self.latest_year}"

    def load(self) -> dict[pd.DataFrame]:
        """Pipeline of loading process"""
        self.get_metadata(self.metadata_path)
        dfs = self.download_dataframes(self.dataframe_path)
        return dfs

    @RepoConnector.close_connection_if_exception
    def get_metadata(self, link):
        """Get metadata information"""
        metadata = pd.read_csv(link)
        self.matchday = metadata[metadata.anno == self.latest_year].giornata.max()

    @RepoConnector.close_connection_if_exception
    def download_dataframes(self, link) -> dict[pd.DataFrame]:
        """Download the dataframes"""
        dict_df = {
            target: pd.read_csv(f"{link}/{self.matchday}/{target}.csv", index_col=0)
            for target in self.targets
        }
        return dict_df
