import pandas as pd
import re
import webbrowser
import requests
from utils.config import VERSION, REPOPATH, CURRENT_YEAR, TARGETS


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
        self.version_path = f"{self.path}/data/versions/versions.csv"
        self.upd_link = f"{self.path}/data/versions/schedina.apk"
        self.line = "Nuovo aggiornamento disponibile."

    def search_update(self) -> bool:
        """Search new updates and, if available, update the app"""
        need_to_update = self.check_update(self.version_path)
        return need_to_update

    @RepoConnector.close_connection_if_exception
    def check_update(self, link):
        """Check the availability of new versions from
        the project's GitHub repository
        """
        versions = pd.read_csv(link)
        self.latest_version = versions[versions["latest"]]["version"].values[0]
        self.no_updated = self.latest_version != self.curr_version
        return self.no_updated

    def update_app(self):
        """Update the app at latest version"""
        webbrowser.open(self.upd_link)


class Loader(RepoConnector):
    """Load the dataframes from the project's GitHub repository"""

    def __init__(self):
        super().__init__()
        self.current_year = CURRENT_YEAR
        self.targets = TARGETS
        self.metadata_path = f"{self.path}/data/metadata.csv"
        self.dataframe_path = f"{self.path}/data/predictions/{self.current_year}"
        self.accessories_path = f"{self.path}/data/accessories"

    def load_dfs(self) -> dict[pd.DataFrame]:
        """Pipeline of loading process"""
        self.get_metadata(self.metadata_path)
        dfs = self.download_dataframes(self.dataframe_path)
        return dfs

    @RepoConnector.close_connection_if_exception
    def get_metadata(self, link):
        """Get metadata information"""
        metadata = pd.read_csv(link)
        self.matchday = metadata[metadata.anno == self.current_year].giornata.max()

    @RepoConnector.close_connection_if_exception
    def download_dataframes(self, link) -> dict[pd.DataFrame]:
        """Download the dataframes"""
        dict_df = {
            target: pd.read_csv(f"{link}/{self.matchday}/{target}.csv", index_col=0)
            for target in self.targets
        }
        return dict_df

    def download_readme(self) -> str:
        url = f"{self.path}/README.md"
        content = requests.get(url).text
        md_to_kv_translator = {
            r"\*\*(.*?)\*\*": r"[b]\1[/b]",  # header 1
            r"# (.*?)(?=\n|$)": r"[size=50]\1[/size]",  # bold
        }
        for md, kv in md_to_kv_translator.items():
            content = re.sub(md, kv, content)
        return content

    def extract_previous_encounters(self):
        df = pd.read_csv(f"{self.accessories_path}/previous_encounters.csv")
        return df

    def load_ranking(self):
        df = pd.read_csv(f"{self.accessories_path}/ranking.csv")
        return df

    def load_momentum(self):
        df = pd.read_csv(f"{self.accessories_path}/previous_encounters.csv")
        df[["casa", "trasferta"]] = df.partita.str.split(" - ", expand=True)
        df = df.sort_values(by=["anno", "giornata"], ascending=False)
        return df
