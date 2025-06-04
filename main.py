import MachineLearning as ML
import forexdataservice as fds

# df = fds.fetch_forex_data()
# print(df)
# ML.graphRawFX()

print(fds.fetch_realtime_forex_polygon())
