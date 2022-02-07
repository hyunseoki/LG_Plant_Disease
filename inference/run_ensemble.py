import csv
import os
import pandas as pd
from src.data_description import labels
import numpy as np


base_dir = './'

csv_dir = os.path.join(base_dir, 'submission')
_csv_saved_dir = os.path.join(base_dir, 'submission')

info_dict = []
dataset = pd.read_csv(
    os.path.join(csv_dir, 'model_001.csv'),
    delimiter=',', header=0
)

print("GET CSV FILES")
for k in range(dataset.__len__()):
    tmp = {'filename': str(dataset['image'][k]),
           'disease_label': 0}
    info_dict.append(tmp)


csv_fn_list = os.listdir(csv_dir)
csv_fn_list = [fn for fn in csv_fn_list if fn.endswith('csv')]
csv_fn_list.sort()

li = []
cnt = 0

for csv_fn in csv_fn_list:
    cnt += 1
    print(csv_fn)
    fn = os.path.join(csv_dir, csv_fn)
    df = pd.read_csv(fn, index_col=0, header=0)
    li.append(df)

frame = pd.concat(li, axis=1, ignore_index=True)
# frame = frame.drop([2, 4], axis=1)
np_df = frame.to_numpy()

dict_keys = list(labels.keys())
dict_values = list(labels.values())

label_np = np.zeros((np_df.shape[0], np_df.shape[1]))
for i in range(np_df.shape[0]):
    for j in range(np_df.shape[1]):
        labels_str = np_df[i][j]
        labels_int = dict_keys[dict_values.index(labels_str)]

        label_np[i][j] = int(labels_int)

ensemble_label = np.zeros(np_df.shape[0])

ccnt = 0
for k in range(np_df.shape[0]):
# for k in range(100):
    tmp = label_np[k]
    values, counts = np.unique(tmp, return_counts=True, axis=0)

    if values.shape[0] == 3:
        freq_values = tmp[1]
    else:
        freq_values = values[np.argmax(counts)]

    # print(values, counts, freq_values)
    if int(freq_values) != int(tmp[1]):
        print(values, counts, freq_values)
        ccnt += 1
    ensemble_label[k] = freq_values

print(ccnt)
# exit()

# ind = np.argmax(counts)
# print(counts.shape)
# ensemble_label = ind[:]
# print(ensemble_label)


with open(os.path.join(_csv_saved_dir, 'final_results.csv'), 'wt') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=["image", "label"])
    writer.writeheader()

    csv_writer = csv.writer(output_file, delimiter=',')

    for _info, pred in zip(info_dict, ensemble_label):
        disease_label = labels[pred]
        csv_writer.writerow([_info["filename"], disease_label])
