# -*- coding: utf-8 -*-

import pandas


def data_categorize():
    reviews_raw = pandas.read_csv('./Data/reviews_US.csv')
    reviews = reviews_raw[["hotel.location", "user.income", "exclamation", "exclamation_merged", "hotel.tags"]].dropna(axis=0, how='any')
    reviews[["user.income", "exclamation"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_income.csv', index=False, encoding='utf-8')
    reviews[["user.income", "exclamation_merged"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_merged_income.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'New_York_City'][["user.income", "exclamation"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_income_New_York_City.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'New_York_City'][["user.income", "exclamation_merged"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_merged_income_New_York_City.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'Los_Angeles'][["user.income", "exclamation"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_income_Los_Angeles.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'Los_Angeles'][["user.income", "exclamation_merged"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_merged_income_Los_Angeles.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    data_categorize()
