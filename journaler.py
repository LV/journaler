"""
Creates a new file upon invokation into the editor and directory of the user's choice

Customizable options:
- Filetype (e.g. `.md`, `.txt`, `.org`)
- Directory (e.g. `~/journaler`)
- Editor (e.g. 

Currently only for Unix systems
"""

import argparse
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
import platform
import time
import tomllib


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Creates new journal entry and opens file in editor of choice")

    parser.add_argument("-d", "--date-format", action="store")
    parser.add_argument("-e", "--editor", action="store")
    parser.add_argument("-f", "--file-ext", action="store")
    parser.add_argument("-j", "--journal-dir", action="store")
    parser.add_argument("-t", "--title", action="store")

    return parser.parse_args()


def get_config_dir_based_on_platform() -> Path:
    # NOTE: As of now no support for a config file in a non-default location
    match platform.system():
        case ("Linux" | "Darwin"):
            return Path(os.getenv('XDG_CONFIG_HOME', str(Path.home() / ".config")))
        case _:
            raise RuntimeError("This platform is currently not supported")

def get_default_journal_dir_based_on_platform() -> Path:
    match platform.system():
        case ("Linux" | "Darwin"):
            return Path.home() / "journal"
        case _:
            raise RuntimeError("This platform is currently not supported")

def get_default_editor() -> str:
    match platform.system():
        case ("Linux" | "Darwin"):
            return os.getenv("EDITOR") or os.getenv("VISUAL") or "nano"
        case "Windows":
            return os.getenv("EDITOR") or os.getenv("VISUAL") or "notepad"
        case _:
            raise RuntimeError("This platform is currently not supported")


@dataclass
class Config:
    date_format: str = "%Y%m%d-%H%M%S" # YYYYMMDD-HHMMSS
    file_extension: str = ".md"
    editor: str = get_default_editor()
    journal_directory: Path = get_default_journal_dir_based_on_platform()
    file_title: str = datetime.now().strftime(date_format)


def get_configuration(args: argparse.Namespace) -> None:
    """
    First, reads from the arguments and sets the variables accordingly

    For any missing arguments, it tries to read from the configuration directory

    Will assign remaining variables from the listed configuration

    If file does not exist, will prompt user and create a config file with all the defaults

    Any unlisted variables in both the args and config will use default values
    """

    is_new_config: bool = False

    ### Default variables
    default_date_format: str = "%Y%m%d-%H%M%S"
    default_file_extension: str = ".md"
    default_editor: str = get_default_editor()
    default_journal_dir: Path = get_default_journal_dir_based_on_platform()

    # Create config file if it doesn't exist
    config_path: Path = get_config_dir_based_on_platform() / "journaler" / "journaler.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.touch(exist_ok=True)

    # Write to config with default values if config file is empty
    if config_path.exists() and config_path.is_file() and config_path.stat().st_size == 0:
        is_new_config = True
        print(f"Config file doesn't exist! Creating default config at {str(config_path)}")
        time.sleep(1) # second
        
        config_data = f"""# This is the default configuration!

date_title_format = "{default_date_format}"
file_extension = "{default_file_extension}"
editor = "{default_editor}"
journal_directory = "{str(default_journal_dir)}"
"""
        config_path.write_text(config_data)

    else:
        with config_path.open("rb") as file:
            config_data = tomllib.load(file)

def main() -> None:
    args = get_args()
    get_configuration(args)

if __name__ == "__main__":
    main()
