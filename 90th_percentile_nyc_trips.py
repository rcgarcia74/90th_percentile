import pandas as pd
import urllib.request

url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet'
local_file = 'yellow_tripdata_2026-01.parquet'

# Download
urllib.request.urlretrieve(url, local_file)

# Load
df = pd.read_parquet(local_file)

# Compute 90th percentile
threshold = df['trip_distance'].quantile(0.9)
print(f"90th percentile distance: {threshold} miles")

# Filter trips above threshold
top_trips = df[df['trip_distance'] > threshold]
print(f"Number of trips above 90th percentile: {len(top_trips):,}")
print(f"Total trips in file: {len(df):,}")

# Show top trips
print(top_trips[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance', 'fare_amount']].head(10))

# Save to CSV if needed
top_trips.to_csv('top_trips_2026-01.csv', index=False)
print("Saved to top_trips_2026-01.csv")