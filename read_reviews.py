# -*- coding: utf-8 -*-

import pandas
import json
import random
import glob
import os
from pandas.io.json import json_normalize
import pandas
import sys


def count_merged(s):
    cnt = 0
    for i in range(len(s)):
        if s[i] == '!' and (i == 0 or s[i - 1] != '!'):
            cnt += 1
    return cnt


def read_reviews():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    cities_dict = dict()
    with open('./Data/Cities_list.txt', 'r') as f:
        for line in f:
            city = line.strip().split()
            cities_dict[city[1]] = city[0]
    os.chdir('./Data/Hotels')
    hotels_dict = dict()
    for filename in glob.glob('*.json'):
        with open(filename, 'r') as f:
            hotel = json.load(f, encoding='utf-8')
            hotel.pop('reviews_list', None)
            hotels_dict[filename[0:-5]] = hotel
    os.chdir('..')
    os.chdir('./Reviews')
    reviews_list = list()
    reviews_list_US = list()
    for filename in glob.glob('*.json'):
        with open(filename, 'r') as f:
            review = json.load(f, encoding='utf-8')
            if review["hotel_id"] not in hotels_dict:
                continue
            review['hotel'] = hotels_dict[review["hotel_id"]]
            review['hotel']['location'] = cities_dict[review['city_id']]
            review['content_length'] = len(str(review['content']))
            review['exclamation'] = str(review['content']).count('!')
            review['exclamation_merged'] = count_merged(str(review['content']))
            review['exclamation_title'] = str(review['title']).count('!')
            review['exclamation_merged_title'] = count_merged(str(review['title']))
            reviews_list.append(review)
            if review['user']['country'] == 'US':
                reviews_list_US.append(review)
    reviews = json_normalize(reviews_list)
    reviews_US = json_normalize(reviews_list_US)
    os.chdir('..')
    reviews.to_csv('reviews.csv', index=False, encoding='utf-8')
    reviews_US.to_csv('reviews_US.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    read_reviews()
