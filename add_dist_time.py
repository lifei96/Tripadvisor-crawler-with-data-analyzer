# -*- coding: utf-8 -*-

from dist_duration import dist_duration
import os
import json
import pandas
import random


def add_dist_duration():
    with open('./distance_key.txt', 'r') as f:
        keys = f.read().split('\n')
    dataset = pandas.read_excel('./Data/reviews_US_no_distance.xlsx')
    dataset = dataset.fillna('')
    row_size = dataset.shape[0]
    for i in range(row_size):
        print '-----'
        print i
        try:
            row = dataset.loc[i]
            if row['driving.distance'] != '' or row['driving.duration'] != '':
                continue
            origin = row['user.location']
            dest = row['hotel.city']
            key = random.sample(keys, 1)[0]
            result_status, element_status, dist, duration = dist_duration(str(origin), str(dest), 'driving', str(key))
            while result_status != 'OK':
                print result_status
                keys.remove(key)
                if len(keys) == 0:
                    print 'no valid keys'
                    return
                key = random.sample(keys, 1)[0]
                result_status, element_status, dist, duration = dist_duration(str(origin), str(dest), 'driving', str(key))
            print result_status, element_status, dist, duration
            if element_status != 'OK':
                print 'element error', element_status
                continue
            dataset.loc[i, 'driving.distance'] = dist
            dataset.loc[i, 'driving.duration'] = duration
            print 'now: ', dataset.loc[i, 'driving.distance'], dataset.loc[i, 'driving.duration']
        except:
            print 'failed'
    dataset.to_csv('./Data/reviews_US_with_distance.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    add_dist_duration()
