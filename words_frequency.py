# -*- coding: utf-8 -*-

import pandas
import csv


def data_categorize():
    words_dict = dict()
    reviews = pandas.read_csv('./Data/reviews.csv')
    for index, row in reviews.iterrows():
        content = str(row['content'])
        for i in range(len(content)):
            if i > 0 and content[i] == '!' and content[i - 1] != '!':
                r = i
                while r > 0 and content[r - 1] == ' ':
                    r -= 1
                l = r - 1
                while l > 0 and content[l - 1] != ' ':
                    l -= 1
                word = content[l:r]
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1
    with open('./Data/words_frequency.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in words_dict.items():
            writer.writerow([key, value])

    words_dict = dict()
    reviews = pandas.read_csv('./Data/reviews_US.csv')
    for index, row in reviews.iterrows():
        content = str(row['content'])
        for i in range(len(content)):
            if i > 0 and content[i] == '!' and content[i - 1] != '!':
                r = i
                while r > 0 and content[r - 1] == ' ':
                    r -= 1
                l = r - 1
                while l > 0 and content[l - 1] != ' ':
                    l -= 1
                word = content[l:r]
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1
    with open('./Data/words_frequency_US.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in words_dict.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    data_categorize()
