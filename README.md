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
Create a python file (90th_percentile_nyc_trips.py). Import pandas and and urllib.request.

```python
import pandas as pd
import urllib.request
```
pandas will be responsible for loading, reading and executing the quantile() function. urllib.request will download the parquet file from a given link.

Download the parquet file. Pick the January Yellow Taxi record.

```python
url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet'
local_file = 'yellow_tripdata_2026-01.parquet'

# Download
urllib.request.urlretrieve(url, local_file)
```
Now load the downloaded parquet file.

```python
df = pd.read_parquet(local_file)
```
Compute the 90th percentile against the trip_distance column

```python
threshold = df['trip_distance'].quantile(0.9)
print(f"90th percentile distance: {threshold} miles")
```
Filter the trips above the threshold.

```python
top_trips = df[df['trip_distance'] > threshold]
print(f"Number of trips above 90th percentile: {len(top_trips):,}")
print(f"Total trips in file: {len(df):,}")
```
Show the top trips from the January record.

```python
print(top_trips[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance', 'fare_amount']].head(10))
```
Save the top trips into a file.

```python
top_trips.to_csv('top_trips_2026-01.csv', index=False)
print("Saved to top_trips_2026-01.csv")
```

## Executing the code
Run the code below, which has the complete code, that will generate the csv file that represents the 90th percentile of the trip for January. 

```bash
python3 90th_percentile_nyc_trips.py
```
This will generate the csv file in the current directory. To verify if the quantile captured the top 10%, the top trips should only show 372,334 which is 9.99% of the total population of the parquet file. To do this, you can install the PyPI version of the parquet-tools to inspect the metadata of the parquet file which shows the total record count.

```bash
pip3 install parquet-tools
```
Add the parquet-tools to PATH. The installed location is on **/Library/Frameworks/Python.framework/Versions/3.13/bin/parquet-tools**.

```bash
# Export parquet-tools (PyPI). Add this to ~/.bash_profile
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"
```
The reload ~/.bash_profile to pickup the latest change in the PATH.

```bash
source ~/.bash_profile
```
Now inspect the parquet file and look for num_rows value under file meta data section.

```bash
 parquet-tools inspect yellow_tripdata_2026-01.parquet | more
```
Here's the expected output.

```bash
############ file meta data ############
created_by: parquet-cpp-arrow version 16.1.0
num_columns: 20
num_rows: 3724889
num_row_groups: 4
format_version: 2.6
serialized_size: 11209


############ Columns ############
VendorID
tpep_pickup_datetime
tpep_dropoff_datetime
passenger_count
trip_distance
RatecodeID
store_and_fwd_flag
PULocationID
DOLocationID
payment_type
fare_amount
extra
mta_tax
tip_amount
tolls_amount
improvement_surcharge
total_amount
congestion_surcharge
```

Trips above 90th Percentile = (372,334 / 3,724,889) * 100 = 9.99%. 
