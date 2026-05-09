# 90th_percentile
NYC Trip Data: distance travelled in 90th percentile

This repo solves this problem: Using NYC “Yellow Taxi” Trips Data, give me all the trips over 0.9 percentile in distance travelled for any of the parquet files you can find there.

## Assumptions
1. One parquet file (https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet)
2. No 3rd party services used
3. No Python Notebook used
4. The only tool & library used for this repo is Python and the pandas package

## Design Decisions
1. Choose a tool or library that will do the job the easiest and fastest.
2. The tool must have a a mature implementation of the quantile function.
3. Print the trips that are the 90th percentile as proof of the function.
4. Run in Macbook, no external services.

## Initial Research
Since the file is in parquet format, parquet-tools/parquet-cli libraries came to mind first but these tools lack the quantile functionality that you have to write your own computation, it's trivial, but Python pandas module can do a better job since you don't have to write a custom function to handle the quantile computation. pandas is a single canonical implementation, open source, and expect consistent results whereas the parquet-* implementation is not. 

## Pre-requisite
The only pre-requisite here are the following Python modules.
- pandas deleagates reading the parquet file to pyarrow , execute quantile() function and filtering rows
- pyarrow for loading and reading the parquet file

In the terminal, install pandas and pyarrow modules.
```bash
python3 -m pip install pandas pyarrow
```

To directly download the parquet file, urlib.request module is needed.

## Code Flow
