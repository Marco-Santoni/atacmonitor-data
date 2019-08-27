import dask.dataframe as dd
import pandas as pd
import numpy as np

trips = dd.read_csv(
    '/home/ubuntu/rome_static_gtfs/trips.txt',
    dtype={'service_id': str},
    usecols=['trip_id', 'service_id', 'route_id']
)
stop_times = dd.read_csv(
    '/home/ubuntu/rome_static_gtfs/stop_times.txt',
    dtype={'stop_id': str},
    usecols=['trip_id', 'stop_id', 'stop_sequence']
)

trips_rep = trips.repartition(npartitions=1)
result = stop_times.merge(trips_rep, on='trip_id')
second_last_stop = result.groupby(['route_id', 'service_id']).stop_sequence.apply(lambda x: x.nlargest(2).min()).reset_index()
second_last_stop = second_last_stop.compute()

df_with_stops = result.merge(second_last_stop).compute()
pd.DataFrame(
    {
        'stop_id': df_with_stops['stop_id'].unique()
    }
).to_csv('unique_stop_id.csv', index=False)

