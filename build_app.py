import subprocess
import pandas as pd
from job.display.utils.config import VERSION as kivy_app_version


def raise_reading_file_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(f"File not found: {kwargs['file_path']}")
        except Exception as e:
            print(f"An error occurred: {e}")

    return wrapper


@raise_reading_file_exception
def get_version_from_versions_csv(file_path):
    versions = pd.read_csv(file_path)
    version = versions.loc[versions.latest, "version"].item()
    return version


@raise_reading_file_exception
def get_version_from_buildozer_spec(file_path):
    version = None
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("version"):
                version = line.split(" = ")[1].replace("\n", "")
                break
    return version


def check_version():
    csv_version = get_version_from_versions_csv(file_path="data/versions/versions.csv")
    buildozer_version = get_version_from_buildozer_spec(file_path="buildozer.spec")
    check = kivy_app_version == csv_version == buildozer_version
    metadata = {
        "kivy_app": kivy_app_version,
        "csv": csv_version,
        "buildozer": buildozer_version,
    }
    return check, metadata


def check_layout():
    with open("job/display/main.py", "r") as file:
        for line in file:
            if "self.sf = " in line:
                scale_factor_line = line
            elif "Window.size = " in line:
                size_line = line
        check = (
            float(scale_factor_line.split(" = ")[1][0:3]) == 1.0 and "#" in size_line
        )
        metadata = {"scale_factor": scale_factor_line, "size": size_line}
        return check, metadata


checks = {"version": check_version(), "layout": check_layout()}
check_output = []
for check in checks.values():
    if check[0]:
        check_output.append(True)
    else:
        check_output.append(check[0])


if all(check_output):
    print("Checks successful. Buildozer ready")
else:
    print("Checks unsuccessful. Exiting")
    print(check_output)
