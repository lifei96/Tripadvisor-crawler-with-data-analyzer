# -*- coding: utf-8 -*-

import os
import time
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


failed_list = list()


def mark_failed(city_name, city_id):
    failed_list.append(city_name + ' ' + city_id)


def crawl(city_name, city_id, url):
    print (city_name + ' ' + city_id)
    driver = webdriver.Chrome(executable_path="./chromedriver")
    time.sleep(6)
    try:
        driver.get(url)
        time.sleep(6)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        mark_failed(city_name, city_id)
        print('-----failed to get url')
        print('-----marked')
        driver.quit()
        return
    try:
        while True:
            driver.find_element_by_xpath("//*[@class='jfy_checkbox reduced_height jfy_checkbox_hotel_class jfy_filter_s_10 ui_input_checkbox']").click()
            checked = driver.find_elements_by_xpath("//*[@class='jfy_checkbox reduced_height jfy_checkbox_hotel_class jfy_filter_s_10 ui_input_checkbox selected']")
            if checked:
                break
        print('-----clicked 5 stars')
        time.sleep(6)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        mark_failed(city_name, city_id)
        print('-----failed to click 5 stars')
        print('-----marked')
        driver.quit()
        return
    hotels_list = list()
    while True:
        flag = True
        try:
            all_hotels = driver.find_elements_by_xpath("//*[@class='listing easyClear  ']")
        except NoSuchElementException:
            print('-----failed to find hotels list')
            break
        for hotel in all_hotels:
            try:
                hotel.find_element_by_xpath("//*[@class='ui_star_rating no_bg star_5']")
                hotel_id = hotel.get_attribute("data-locationid")
                hotels_list.append(hotel_id)
            except NoSuchElementException:
                flag = False
                continue
        try:
            imperfect = driver.find_elements_by_xpath("//*[@class='listing easyClear  p13n_imperfect ']")
            if imperfect:
                flag = False
        except:
            print('-----no imperfect hotels')
        if not flag:
            break
        try:
            next_page = driver.find_element_by_xpath("//*[@class='nav next ui_button primary taLnk']").get_attribute("href")
            driver.get(next_page)
            time.sleep(6)
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print('-----failed to click next page')
            break
        try:
            driver.find_element_by_xpath("//*[@class='ui_close_x']").click()
        except:
            print('-----no x')
    city = dict()
    city['city_name'] = city_name
    city['city_id'] = city_id
    city['hotels_list'] = hotels_list
    with open('./Data/Cities/' + city_name + '-' + city_id + '.txt', 'w') as f:
        f.write(json.dumps(city, indent=4))
    time.sleep(6)
    driver.quit()


if __name__ == '__main__':
    if not os.path.exists('./Data/Cities'):
        os.mkdir('./Data/Cities')
    if not os.path.exists('./Data/Hotels'):
        os.mkdir('./Data/Hotels')
    with open('./Data/Cities_list.txt', 'r') as f:
        cities_info = f.read().split('\n')
        cities_list = list()
        for city in cities_info:
            cities_list.append(city.split(' '))
    for city in cities_list:
        crawl(city[0], city[1], 'https://www.tripadvisor.com/Hotels-g' + city[1])
    with open('./Data/cities_failed_list.txt', 'w') as f:
        f.write('\n'.join(failed_list))
