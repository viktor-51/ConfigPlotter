import glob 

import numpy as NP
import pandas as p

falulty_headers = ["iowait(post)", "interrupts"]
h = list(range(0, 23))

l = glob.glob("*/*/cpu_data.csv")

print("path", l)

for n in l:
    df_idx = p.read_csv(n, names = h).to_numpy()
    df_h = p.read_csv(n)

    nbr_columns = df_idx.shape[-1]
    headers = df_h.columns

    sh = df_idx.shape

    sh_n = (sh[0] - 1, sh[1] - 2)
    new_data = NP.zeros(sh_n)

    inc = 0
    go = False

    idx_correct = 0
    for false_idx in range(0, nbr_columns):
        correct_header = headers[idx_correct]

        if go or (not correct_header in falulty_headers): 
            new_data[:, idx_correct] = df_idx[1 :, false_idx]
            idx_correct += 1
        else:
            inc += 1
            if inc == 2:
                go = True

    df = p.DataFrame(data = new_data, columns = headers)
    df.to_csv(path_or_buf = n, index = False)
