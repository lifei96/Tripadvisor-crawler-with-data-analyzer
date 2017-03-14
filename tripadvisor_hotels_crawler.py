# -*- coding: utf-8 -*-

import os
import time
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


failed_list = list()

failed_review_list = list()


def mark_failed(city_id, city_name, hotel_id):
    failed_list.append(city_id + ' ' + city_name + ' ' + hotel_id)


def mark_failed_review(review_id):
    failed_review_list.append(review_id)


def crawl(city_id, city_name, hotel_id, url):
    print (city_name + ' ' + city_id + ' ' + hotel_id)
    driver = webdriver.Chrome(executable_path="./chromedriver")
    time.sleep(3)
    try:
        driver.get(url)
        time.sleep(5)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        mark_failed(city_id, city_name, hotel_id)
        print('-----failed to get url')
        print('-----marked')
        driver.quit()
        return
    try:
        driver.find_element_by_xpath("//*[@class='ui_close_x']").click()
    except:
        print('-----no x')
    hotel_data = dict()
    reviews_list = list()
    while True:
        try:
            while True:
                driver.find_element_by_xpath("//*[@onclick=ta.prwidgets.call(\'handlers.clickExpand\',event,this);']").click()
                try:
                    driver.find_element_by_xpath("//*[@class='ui_close_x']").click()
                except:
                    print('-----no x')
                time.sleep(1)
                checked = driver.find_elements_by_xpath("//*[@onclick='ta.prwidgets.call(\'handlers.clickCollapse\',event,this);']")
                if checked:
                    break
            print('-----clicked More')
            time.sleep(5)
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            mark_failed(city_id, city_name, hotel_id)
            print('-----failed to click More')
            print('-----marked')
            driver.quit()
            return
        try:
            all_reviews = driver.find_elements_by_xpath("//*[@class='reviewSelector']")
        except NoSuchElementException:
            print('-----failed to find reviews list')
            break
        for review in all_reviews:
            review_data = dict()
            user_data = dict()
            review_data['hotel_id'] = hotel_id
            review_data['city_id'] = city_id
            try:
                review_id = review.get_attribute("data-reviewId")
                reviews_list.append(review_id)
                review_data['review_id'] = review_id
                review_title = review.find_elements_by_xpath("//*[@class='noQuotes']")
                if review_title:
                    review_data['title'] = review_title[0].text
                else:
                    review_data['title'] = ''
                review_content = review.find_elements_by_xpath("//p[]")
                if review_content:
                    review_data['content'] = review_content[0].text
                else:
                    review_data['content'] = ''
                review_date = review.find_elements_by_xpath("//*[@class='ratingDate relativeDate']")
                if review_date:
                    review_data['date'] = review_date[0].get_attribute('title')
                else:
                    review_data['date'] = ''
                review_rating = review.find_elements_by_xpath("//*[@class='rating reviewItemInline']")
                if review_rating:
                    rating_str = review_rating[0].find_elements_by_xpath("//span[]")[0].get_attribute('class')
                    review_data['rating'] = int(rating_str[-2:]) / 10.0
                else:
                    review_data['rating'] = ''
                user = review.find_element_by_xpath("//*[@class='member_info']")
                user_name = user.find_elements_by_xpath("//*[@class='expand_inline scrname']")
                if user_name:
                    user_data['name'] = user_name[0].text
                else:
                    user_data['name'] = ''
                user_location = user.find_elements_by_xpath("//*[@class='location']")
                if user_location:
                    user_data['location'] = user_location[0].text
                else:
                    user_data['location'] = ''
            except:
                mark_failed_review(review_id)
                print ("-----failed to retrieve review " + review_id)
            review_data['user'] = user_data
            with open('./Data/Reviews/' + review_id + '.txt', 'w') as f:
                f.write(json.dumps(review_data, indent=4))
        try:
            next_page = driver.find_element_by_xpath("//*[@class='nav next rndBtn ui_button primary taLnk']").get_attribute("href")
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
    hotel_data['reviews_list'] = reviews_list
    with open('./Data/Hotels/' + hotel_id + '.txt', 'w') as f:
        f.write(json.dumps(hotel_data, indent=4))
    time.sleep(6)
    driver.quit()


if __name__ == '__main__':
    if not os.path.exists('./Data/Hotels'):
        os.mkdir('./Data/Hotels')
    if not os.path.exists('./Data/Reviews'):
        os.mkdir('./Data/Reviews')
    with open('./Data/Cities_list.txt', 'r') as f:
        cities_info = f.read().split('\n')
        cities_list = list()
        for city in cities_info:
            cities_list.append(city.split(' '))
    for city in cities_list:
        with open('./Data/Cities/' + city[0] + '-' + city[1] + '.txt', 'r') as f:
            hotels_info = json.loads(f.read())
        for hotel_id in hotels_info["hotels_list"]:
            crawl(city[1], city[0], hotel_id, 'https://www.tripadvisor.com/Hotel_Review-g' + city[1] + '-d' + hotel_id + '-Reviews')
    with open('./Data/cities_failed_list.txt', 'w') as f:
        f.write('\n'.join(failed_list))
    with open('./Data/reviews_failed_list.txt', 'w') as f:
        f.write('\n'.join(failed_review_list))
