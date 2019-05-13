
import os
import glob
import pandas as pd

#  set target for price prediction
#  target == close price on today + DAYS_AHEAD
DAYS_AHEAD = 2

os.chdir("tmp/")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
target_rows = 0

for f in all_filenames:
    df = pd.read_csv(f, index_col=False)

    if target_rows == 0:
        target_rows = df.count()[0]

    row_count = df.count()[0]
    if row_count != target_rows:
        print("ROW ERROR: " + f + ' ROWS: ' + str(row_count) + " TARGET ROWS: " + str(target_rows))
        continue

    next_day_close = df['close']
    next_day_close = next_day_close.drop(range(DAYS_AHEAD))

    df = df.drop(range(target_rows - DAYS_AHEAD, target_rows))
    df['Target_Close_Plus_' + str(DAYS_AHEAD)] = next_day_close.values

# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
# os.chdir("../")
# combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')

print('Fin')