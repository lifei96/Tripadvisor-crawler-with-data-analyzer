# -*- coding: utf-8 -*-

import pandas


def data_categorize():
    reviews = pandas.read_csv('./Data/reviews_US.csv')
    reviews[["user.income", "exclamation", "hotel.reviews_count"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_income.csv', index=False, encoding='utf-8')
    reviews[["user.income", "exclamation_merged", "hotel.reviews_count"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_merged_income.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'New_York_City'][["user.income", "exclamation", "hotel.reviews_count"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_income_New_York_City.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'New_York_City'][["user.income", "exclamation_merged", "hotel.reviews_count"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_merged_income_New_York_City.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'Los_Angeles'][["user.income", "exclamation", "hotel.reviews_count"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_income_Los_Angeles.csv', index=False, encoding='utf-8')
    reviews[reviews['hotel.location'] == 'Los_Angeles'][["user.income", "exclamation_merged", "hotel.reviews_count"]].dropna(axis=0, how='any').to_csv('./Data/exclamation_merged_income_Los_Angeles.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    data_categorize()
