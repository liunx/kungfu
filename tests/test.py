#!/usr/bin/env python

import pickle
import pprint


if __name__ == '__main__':
    data1 = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
    output = open('data.pkl', 'wb')
    pickle.dump(data1, output)
    output.close()

    pkl_file = open('data.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    print(data1)
    #pprint.pprint(data1)

    pkl_file.close()
