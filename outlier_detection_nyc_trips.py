"""
NYC Yellow Taxi Trip Distance - Outlier Summary
Outputs only the summary table of outlier counts.
Reads parquet directly from the TLC CloudFront URL (no local file).
"""

import pandas as pd
import numpy as np

URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet'

# Thresholds
MAX_PLAUSIBLE_DISTANCE_MI = 100
MAX_PLAUSIBLE_DURATION_MIN = 1440
MAX_PLAUSIBLE_SPEED_MPH = 100
MIN_FARE_FOR_ZERO_DISTANCE = 2.50


def main() -> None:
    df = pd.read_parquet(URL,
                         columns=['tpep_pickup_datetime',
                                  'tpep_dropoff_datetime',
                                  'trip_distance',
                                  'fare_amount'])

    duration_min = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60.0
    speed_mph = pd.Series(
        np.where(duration_min > 0,
                 df['trip_distance'] / (duration_min / 60.0),
                 np.nan),
        index=df.index
    )

    rules = {
        'Zero or negative distance':        df['trip_distance'] <= 0,
        'Implausible distance (>100 mi)':   df['trip_distance'] > MAX_PLAUSIBLE_DISTANCE_MI,
        'Invalid duration (<=0 min)':       duration_min <= 0,
        'Excessive duration (>24 hr)':      duration_min > MAX_PLAUSIBLE_DURATION_MIN,
        'Impossible speed (>100 mph)':      speed_mph > MAX_PLAUSIBLE_SPEED_MPH,
        'Negative fare':                    df['fare_amount'] < 0,
        'Zero distance but fare charged':   (df['trip_distance'] == 0) & (df['fare_amount'] > MIN_FARE_FOR_ZERO_DISTANCE),
    }

    total = len(df)
    any_flag = pd.Series(False, index=df.index)
    for mask in rules.values():
        any_flag |= mask.fillna(False)

    # Print summary table
    print(f"{'Outlier rule':<40} {'Count':>12} {'% of total':>12}")
    print('-' * 66)
    for name, mask in rules.items():
        count = int(mask.sum())
        pct = count / total * 100
        print(f"{name:<40} {count:>12,} {pct:>11.3f}%")
    print('-' * 66)
    print(f"{'Total unique outliers':<40} {int(any_flag.sum()):>12,} {any_flag.mean()*100:>11.3f}%")
    print(f"{'Total trips':<40} {total:>12,}")


if __name__ == '__main__':
    main()