# CookBook

Personal project for managing recipes and favorite food!

A desktop app for keeping track of the food you like, the restaurants you rate,
the recipes you cook, and the things you still want to try.

## Features

- **Food Ranking** — rate dishes 0–10, sorted automatically, with a tier list view (SS through F)
- **Restaurants** — rate restaurants 0–5
- **Recipes** — full recipes with ingredients (amount, unit, calories, notes), cook time, and instructions
- **Try Later** — a wishlist of things to try, with one-click move into Food Ranking once you've had them
- **Import from URL** — paste a link to a recipe page and it pulls in the title, ingredients, time, and
  instructions automatically

All data is stored locally in a SQLite file (`cookbook.db`) that's created automatically on first run.
Nothing is uploaded anywhere, and each person who runs the app gets their own separate database.

## Requirements

- Python 3.9 or newer
- Tkinter (bundled with most Python installs; on some Linux distros install `python3-tk` separately)

## Setup

Clone the repo and install the dependencies:

```bash
pip install -r requirements.txt
```

That installs:

| Package | Used for |
|---|---|
| `requests` | fetching recipe pages for URL import |
| `recipe-scrapers` | extracting recipe data from a page's markup |
| `ingredient-parser-nlp` | splitting ingredient lines into name / amount / unit / notes |

Only the Import-from-URL feature needs these — everything else runs on the standard library alone.

## Running

From the project root:

```bash
python main.py
```

The database file is created next to wherever you run the command from, so run it from the project
root to keep `cookbook.db` in the same place each time.

## Project structure

```
CookBook/
  main.py              entry point — opens the connection, builds everything, starts the app
  requirements.txt
  models/              the data layer: what a recipe/ingredient/ranking is and the rules around it
  database/            SQLite storage — one storage class per model, plus table setup
  services/            recipe importing (fetching + parsing)
  ui/                  Tkinter screens — one file per page
```

The layers stay separate on purpose: `ui/` only calls methods on `models/`, and `models/` only talks
to `database/` through its storage object. That means storage can change without touching the UI.
