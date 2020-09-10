# Google Keep Helper Functions

`Python 3.8`: [![Build Status](https://travis-ci.org/kyhau/google-keep-helper.svg?branch=master)](https://travis-ci.org/kyhau/google-keep-helper)

Some Python scripts for managing Google Keep Notes and Lists.

1. [`import_html_to_google_keep.py`](import_html_to_google_keep.py)

    - Import links from a html page to Google Keep as Notes.
    - This script can be used to import bookmarks from Pocket [getpocket.com](https://getpocket.com) to Google Keep.

1. [`remove_duplicates_in_google_keep.py`](remove_duplicates_in_google_keep.py)

    - Find and remove duplicates in Google Keep.


## Build

Linux

```
virtualenv -p python3.8 env
. env/bin/activate
python -m pip install -r requirements.txt

```

Windows

```
virtualenv -p <path-to-python3.8> env
env\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

```
python import_html_to_google_keep.py GOOGLE_USER_NAME GOOGLE_PW HTML_FILE [--dryrun]
```
