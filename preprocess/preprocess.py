# -*- coding: utf-8 -*- 

# 사용 라이브러리 호출
import numpy as np
import pandas as pd
from glob import glob
import json
import re
from chatspace import ChatSpace
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils import *

# raw에서 데이터 호출
@timeit
def load_nsmc_data():
    # data load
    paths = [path.replace('\\', '/') for path in glob('../raw/nsmc/raw/*.json')]
    res = []
    for path in paths:
        with open(path, encoding='utf-8') as data_file:
            res.extend(json.load(data_file))
    # struct dataframe
    data = pd.DataFrame(res)
    # make label
    data['year'] = data['date'].map(lambda x : x.split('.')[0])
    data['rating'] = data['rating'].astype(int)
    data['class'] = np.where(data['rating'].values >= 8, 'POS', 
                           np.where(data['rating'].values >= 4, 'NEU', 'NEG'))
    # drop null data & \n, \r
    data['review'] = data['review'].map(lambda x : re.sub('[\n\r]', '', x))
    data = data[data['review'].map(lambda x : len(x) != 0)]
    return data

# Crawling Data Load
def load_crawled_data():
    pass

@timeit
def spacing(series, spacer):
    return series.map(lambda x : spacer.space(x)).values

# @timeit
# def test():
#     res = []
#     for i in range(100000):
#         res.append(i)

def main():
    data = load_nsmc_data()
#     test()
    spacer = ChatSpace()
    df['review'] = spacing(df['review'], spacer)
    df.to_csv('spacing_nsmc_data.csv')
    
if __name__ == '__main__':
    main()