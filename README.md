<p align="center">
  <img width="300" height="300" src="https://raw.githubusercontent.com/LV/journaler/80f21cbd3f0ba8b95795da5d96d35aad449596dc/assets/logo_white.png">
  <p align="center"><em>A quick command to create new entries in your preferred editor</em></p>
</p>

## Getting started
1. Copy or move the program to a directory of your choice (highly recommended to add this directory to `$PATH`)
```sh
mv journaler.py /usr/local/bin/journaler
```

2. Add execution privileges to journaler
```sh
chmod +x /usr/local/bin/journaler
```

3. Run the program
```sh
journaler
```

## The program
### What is it?

Journaler, upon being invoked, will create a new entry and will open the entry in the editor of choice.

### Running the program

To run the program, just run

```sh
journaler
```

and it will create a new entry. The title of this file will be the date and time from which the program was invoked, unless otherwise specified. Here are the full options as seen by `journaler -h`:
```
usage: journaler.py [-h] [-d DATE_FORMAT] [-e EDITOR] [-f FILE_EXT] [-j JOURNAL_DIR] [-t TITLE] [positional_title]

Creates new journal entry and opens file in editor of choice

positional arguments:
  positional_title      The title of the file

options:
  -h, --help            show this help message and exit
  -d DATE_FORMAT, --date-format DATE_FORMAT
                        Specify the date string format for dated filename entries
  -e EDITOR, --editor EDITOR
                        Specify the editor of choice to open the entry in
  -f FILE_EXT, --file-ext FILE_EXT
                        Specify file extension of the entry
  -j JOURNAL_DIR, --journal-dir JOURNAL_DIR
                        Specify the directory from which this entry should be created in
  -t TITLE, --title TITLE
                        Specify the title
```

### The config file

This project uses a TOML config file. Journaler will read from the `$XDG_CONFIG_HOME/journaler/journaler.toml` file for the settings. If a config file is not found there, it will automatically generate one with all configuration options being set to default values

Below are all available options with their descriptions, default values, and examples.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `date_file_format` | String | `"%Y-%m-%d_%H-%M-%S"` | String format for the dated entry filename
| `file_extension` | String | `".md"` | The desired file extension for your entry
| `editor` | String | `$EDITOR` if it exists, otherwise `$VISUAL`, otherwise `nano` | The desired program to open upon creating a new entry
| `journal_directory` | String | `~/journal` | The directory from which to create the entries from

#### Example Configuration
Note that this is the default configuration
```toml
date_title_format = "%Y-%m-%d_%H-%M-%S"
file_extension = ".md"
editor = "nvim"
journal_directory = "~/journal"
```

#### Notes
- All options are case-sensitive.
- String values should be enclosed in double quotes.
