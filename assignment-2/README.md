# Assignment 2: Beggars Pizza survey

Survey data from Beggars Pizza customers (35 responses, Sept 21 to Oct 20, 2026). The full writeup is in `report.md`.

## Run it

Install the packages:

    python3 -m pip install pandas altair vl-convert-python

Run each script from the `assignment-2` folder:

    python3 code/01_clean.py
    python3 code/02_explore.py
    python3 code/03_directions.py
    python3 code/04_interactive.py
    python3 code/05_iterations.py
    python3 code/06_final.py

## What's in here

- `data/original/`: the survey export, unchanged
- `data/processed/survey_clean.csv`: the cleaned data
- `code/`: one script per step (01 is Task 2, 02 is Task 3, 03 is Task 4, 04 is Task 5, 05 is Task 6, 06 is Task 7)
- `figures/`: charts and screenshots used in the report
- `visualization.html`: the working visualization for Assignment 3. Open it in a browser and click a bar.
