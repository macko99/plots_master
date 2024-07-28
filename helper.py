import pandas as pd

# use this function to extract the data from the csv files
# obtained from the continnum benchamrk
# than avrage the data among rhe runs and place results into data.py
file = '2024-07-16_16:05:48_dataframe_resources.csv'

dir = file.split('_')[0].split('-')[2] + '.' + file.split('_')[0].split('-')[1] + '/'

file_path = dir + file
data = pd.read_csv(file_path)

# Find the maximum value in the "cloud0_memory" column
max_cloud0_memory = data['cloud0_memory'].max()
min_cloud0_memory = data['cloud0_memory'].min()

print(f'The maximum value in the "cloud0_memory" column is: {max_cloud0_memory}')
print(f'The minimum value in the "cloud0_memory" column is: {min_cloud0_memory}')
# substruct
substruct = max_cloud0_memory - min_cloud0_memory
print(f'diff is: {substruct}')

file2 = file.split('_')[0] + "_" + file.split('_')[1] + "_sort_dataframe_56.csv"

file_path2 = dir + file2
data = pd.read_csv(file_path2)

# Find the maximum value in the "cloud0_memory" column
start_time = data['started_application (s)'].max()
start_time = str(start_time).replace('.',',')

print(f'The maximum value in the "started_application (s)" column is: {start_time}')

file3 = file.split('.csv')[0] + "_os.csv"

file_path3 = dir + file3
data = pd.read_csv(file_path3)

# filter data to rows where "memory-used cloud0_mkozub (%)" has value
data = data[data['memory-used cloud0_mkozub (%)'].notnull()]

min_free_mem= data['free memory (KB)'].min()
max_free_mem = data['free memory (KB)'].max()

substruct = (max_free_mem - min_free_mem) / 1024
print(f'memory used (OS) is: {substruct}')