import numpy as np
import pandas as pd
id_data = pd.read_csv('../datafile/node.csv', header=None)
arr = np.load('../datafile/table.npy')


def rank(input_data):
    point = np.zeros(len(arr))
    location = np.zeros(len(input_data))

    for i in range(len(input_data)):
        for j in range(len(id_data[0])):
            if input_data[i] == id_data[0][j]:
                location[i] = j
                break

    for i in range(len(input_data)):
        for j in range(len(arr)):
            point[j] += arr[int(location[i])][j]

    best = np.zeros(5)
    m = 0
    min = 10000000

    for i in range(len(point)):
        if i < 5:
            if point[m] > point[i]:
                m = i
            best[i] = i

        else:
            if point[m] < point[i]:
                best[m] = i

                for j in range(len(best)):
                    if point[int(best[m])] > point[int(best[j])]:
                        m = j

    return best