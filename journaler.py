#!/usr/bin/env python3

"""
Creates a new file upon invokation into the editor and directory of the user's choice

Customizable options:
- Filetype (e.g. `.md`, `.txt`, `.org`)
- Directory (e.g. `~/journaler`)
- Editor (e.g. 

Currently only for Unix systems
"""

import argparse
import os
import platform
import subprocess
import time
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Creates new journal entry and opens file in editor of choice"
    )

    # Optional arguments
    parser.add_argument("-d", "--date-format", action="store", help="Specify the date string format for dated filename entries")
    parser.add_argument("-e", "--editor", action="store", help="Specify the editor of choice to open the entry in")
    parser.add_argument("-f", "--file-ext", action="store", help="Specify file extension of the entry")
    parser.add_argument("-j", "--journal-dir", action="store", help="Specify the directory from which this entry should be created in")

    # Optional `-t` argument for title
    parser.add_argument("-t", "--title", action="store", help="Specify the title")

    # Positional argument for title (acts like `-t` if provided)
    parser.add_argument("positional_title", nargs="?", help="The title of the file")

    args = parser.parse_args()

    if args.title and args.positional_title:
        parser.error("Specify either the title without the `-t` or with `-t`, not both")

    if args.positional_title:
        args.title = args.positional_title

    return args


def get_config_dir_based_on_platform() -> Path:
    # NOTE: As of now no support for a config file in a non-default location
    match platform.system():
        case "Linux" | "Darwin":
            return Path(os.getenv("XDG_CONFIG_HOME", str(Path.home() / ".config")))
        case _:
            raise RuntimeError("This platform is currently not supported")


def get_default_journal_dir_based_on_platform() -> Path:
    match platform.system():
        case "Linux" | "Darwin":
            return Path.home() / "journal"
        case _:
            raise RuntimeError("This platform is currently not supported")


def get_default_editor() -> str:
    match platform.system():
        case "Linux" | "Darwin":
            return os.getenv("EDITOR") or os.getenv("VISUAL") or "nano"
        case "Windows":
            return os.getenv("EDITOR") or os.getenv("VISUAL") or "notepad"
        case _:
            raise RuntimeError("This platform is currently not supported")


@dataclass
class Config:
    date_format: str
    file_extension: str
    editor: str
    journal_directory: Path
    file_title: str | None


def get_configuration(args: argparse.Namespace) -> Config:
    """
    First, reads from the arguments and sets the variables accordingly

    For any missing arguments, it tries to read from the configuration directory

    Will assign remaining variables from the listed configuration

    If file does not exist, will prompt user and create a config file with all the defaults

    Any unlisted variables in both the args and config will use default values
    """

    ### Default variables
    default_date_format: str = "%Y-%m-%d_%H-%M-%S"
    default_file_extension: str = ".md"
    default_editor: str = get_default_editor()
    default_journal_dir: Path = get_default_journal_dir_based_on_platform()

    # Create config file if it doesn't exist
    config_path: Path = (
        get_config_dir_based_on_platform() / "journaler" / "journaler.toml"
    )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.touch(exist_ok=True)

    # Write to config with default values if config file is empty
    if (
        config_path.exists()
        and config_path.is_file()
        and config_path.stat().st_size == 0
    ):
        print(
            f"Config file doesn't exist! Creating default config at {str(config_path)}"
        )
        time.sleep(1)  # second

        config_text_data = f"""# This is the default configuration!

date_title_format = "{default_date_format}"
file_extension = "{default_file_extension}"
editor = "{default_editor}"
journal_directory = "{str(default_journal_dir)}"
"""
        config_path.write_text(config_text_data)

        return Config(
            date_format=(
                args.date_format
                if args.date_format is not None
                else default_date_format
            ),
            file_extension=(
                args.file_ext if args.file_ext is not None else default_file_extension
            ),
            editor=(args.editor if args.editor is not None else default_editor),
            journal_directory=(
                Path(args.journal_dir)
                if args.journal_dir is not None
                else default_journal_dir
            ),
            file_title=args.title,
        )

    ### Config variables
    date_format: str
    file_extension: str
    editor: str
    journal_dir: Path

    with config_path.open("rb") as file:
        config_data = tomllib.load(file)

    if args.date_format is not None:
        date_format = args.date_format
    else:
        if config_data["date_title_format"] is not None:
            date_format = config_data["date_title_format"]
        else:
            date_format = default_date_format

    if args.file_ext is not None:
        file_extension = args.file_ext
    else:
        if config_data["file_extension"] is not None:
            file_extension = config_data["file_extension"]
        else:
            file_extension = default_file_extension

    if args.editor is not None:
        editor = args.editor
    else:
        if config_data["editor"] is not None:
            editor = config_data["editor"]
        else:
            editor = default_editor

    if args.journal_dir is not None:
        journal_dir = Path(args.journal_dir)
    else:
        if config_data["journal_directory"] is not None:
            journal_dir = Path(config_data["journal_directory"])
        else:
            journal_dir = default_journal_dir

    return Config(
        date_format=date_format,
        file_extension=file_extension,
        editor=editor,
        journal_directory=journal_dir,
        file_title=args.title,
    )


def create_and_open_entry(config: Config) -> None:
    filename: str = (
        (config.file_title + config.file_extension)
        if config.file_title is not None
        else (datetime.now().strftime(config.date_format) + config.file_extension)
    )

    config.journal_directory.mkdir(parents=True, exist_ok=True)

    file_path: Path = config.journal_directory / filename
    file_path.touch()

    subprocess.run([config.editor, str(file_path)])


def main() -> None:
    args = get_args()
    config: Config = get_configuration(args)
    create_and_open_entry(config)


if __name__ == "__main__":
    main()
