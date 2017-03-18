# -*- coding: utf-8 -*-

import os
import time
import json
import random
import locale
import geocoder
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


failed_list = list()

failed_review_list = list()


def mark_failed(city_id, city_name, hotel_id):
    failed_list.append(city_id + ' ' + city_name + ' ' + hotel_id)


def mark_failed_review(review_id):
    failed_review_list.append(review_id)


def crawl(driver, driver2, driver3, city_id, city_name, hotel_id, url):
    with open('./geocoding_key.txt', 'r') as f:
        Keys = f.read().split('\n')
    while '' in Keys:
        Keys.remove('')
    print (city_name + ' ' + city_id + ' ' + hotel_id)
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
        return
    try:
        driver.find_element_by_xpath("//*[@class='ui_close_x']").click()
    except:
        print('-----no x')
    hotel_data = dict()
    hotel_name = driver.find_element_by_xpath("//*[@id='HEADING']")
    hotel_data['name'] = hotel_name.text
    print (hotel_data['name'])
    driver3.get('https://www.google.com/search?q=' + hotel_data['name'])
    time.sleep(2)
    try:
        google_header = driver3.find_element_by_xpath("//*[@class='_A8k']")
        google_rating = float(google_header.find_element_by_xpath(".//*[@class='rtng']").text)
        hotel_data['google_rating'] = google_rating
        print (hotel_data['google_rating'])
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        hotel_data['google_rating'] = ''
        print ('no google rating')
    try:
        price = driver3.find_elements_by_xpath("//*[@class='_V0p']")
        hotel_data['price'] = int(price[0].text[1:])
        print (hotel_data['price'])
    except:
        hotel_data['price'] = ''
        print ('no price')
    hotel_header = driver.find_element_by_xpath("//*[@class='headingWrapper easyClear ']")
    try:
        rating = float(hotel_header.find_element_by_xpath(".//*[@property='ratingValue']").get_attribute('content'))
        hotel_data['rating'] = rating
    except:
        hotel_data['rating'] = ''
    try:
        rank = int(hotel_header.find_element_by_xpath(".//*[@class='rank']").text[1:])
        hotel_data['rank'] = rank
    except:
        hotel_data['rank'] = ''
    try:
        reviews_count = int(hotel_header.find_element_by_xpath(".//*[@property='reviewCount']").get_attribute('content'))
        hotel_data['reviews_count'] = reviews_count
    except:
        hotel_data['reviews_count'] = ''
    try:
        if hotel_header.find_elements_by_xpath(".//*[@class='ui_icon certificate-of-excellence']"):
            hotel_data['certificate_of_excellence'] = 1
        else:
            hotel_data['certificate_of_excellence'] = 0
    except:
        hotel_data['certificate_of_excellence'] = 0
    try:
        greenleader = hotel_header.find_elements_by_xpath(".//*[@class='greenLeaderLabelLnk taLnk']")
        if greenleader:
            hotel_data['green_leader'] = greenleader[0].text
        else:
            hotel_data['green_leader'] = ''
    except:
        hotel_data['green_leader'] = ''
    try:
        street_address = hotel_header.find_element_by_xpath(".//*[@property='streetAddress']").text
        hotel_data['street_address'] = street_address
    except:
        hotel_data['street_address'] = ''
    try:
        city = hotel_header.find_element_by_xpath(".//*[@property='addressLocality']").text
        hotel_data['city'] = city
    except:
        hotel_data['city'] = ''
    try:
        state = hotel_header.find_element_by_xpath(".//*[@property='addressRegion']").text
        hotel_data['state'] = state
    except:
        hotel_data['state'] = ''
    try:
        zipcode = hotel_header.find_element_by_xpath(".//*[@property='postalCode']").text
        hotel_data['zipcode'] = zipcode
    except:
        hotel_data['zipcode'] = ''
    property_tags = driver.find_element_by_xpath("//*[@class='property_tags_wrap ']")
    try:
        hotel_class = property_tags.find_element_by_xpath(".//*[@title='Hotel class']").get_attribute("class")
        hotel_data['class'] = int(hotel_class[-2:-1])
    except:
        hotel_data['class'] = ''
    try:
        hotel_tags = property_tags.find_elements_by_xpath(".//*[@class='tag']")
        tags = list()
        for tag in hotel_tags:
            tags.append(tag.text)
        hotel_data['tags'] = tags
    except:
        hotel_data['tags'] = list()
    page_num_list = driver.find_elements_by_xpath("//*[@class='pageNum taLnk']")
    page_num = 1
    for page_num_item in page_num_list:
        page_num_int = int(page_num_item.get_attribute("data-page-number"))
        if page_num_int > page_num:
            page_num = page_num_int
    reviews_list = list()
    for page_num_int in range(page_num):
        try:
            print('-----page ' + str(page_num_int))
            driver.get('https://www.tripadvisor.com/Hotel_Review-g' + city_id + '-d' + hotel_id + '-Reviews-or' + str(page_num_int) + '0')
            time.sleep(5)
            try:
                time.sleep(2)
                driver.find_element_by_xpath("//*[@class='ui_close_x']").click()
            except:
                print('-----no x')
            while True:
                More = driver.find_elements_by_xpath("//*[@class='taLnk ulBlueLinks']")
                time.sleep(2)
                try:
                    time.sleep(2)
                    driver.find_element_by_xpath("//*[@class='ui_close_x']").click()
                except:
                    print('-----no x')
                if More and More[0].text[0] == 'M':
                    try:
                        time.sleep(1)
                        More[0].click()
                        print('-----clicked More')
                        break
                    except:
                        try:
                            time.sleep(2)
                            driver.find_element_by_xpath("//*[@class='ui_close_x']").click()
                        except:
                            print('-----no x')
                else:
                    break
            time.sleep(5)
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            mark_failed(city_id, city_name, hotel_id)
            print('-----failed to click More')
            print('-----marked')
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
                review_title = review.find_elements_by_xpath(".//*[@class='noQuotes']")
                if review_title:
                    review_data['title'] = review_title[0].text
                else:
                    review_data['title'] = ''
                review_content = review.find_elements_by_xpath(".//*[@class='entry']")
                if review_content:
                    review_data['content'] = review_content[0].text
                else:
                    review_data['content'] = ''
                review_date = review.find_elements_by_xpath(".//*[@class='ratingDate relativeDate']")
                if review_date:
                    review_data['date'] = review_date[0].get_attribute('title')
                else:
                    review_data['date'] = ''
                review_rating = review.find_elements_by_xpath(".//*[@class='rating reviewItemInline']")
                if review_rating:
                    flag = False
                    for rating in range(6):
                        if review_rating[0].find_elements_by_xpath(".//span[@class='ui_bubble_rating bubble_" + str(rating) + "0']") :
                            review_data['rating'] = rating
                            flag = True
                            print (rating)
                    if not flag:
                        review_data['rating'] = ''
                else:
                    review_data['rating'] = ''
                if review.find_elements_by_xpath(".//*[@class='mgrRspnInline']"):
                    review_data['replied'] = 1
                else:
                    review_data['replied'] = 0
                user = review.find_element_by_xpath(".//*[@class='member_info']")
                user_name = user.find_elements_by_xpath(".//*[@class='expand_inline scrname']")
                if user_name:
                    user_data['name'] = user_name[0].text
                else:
                    user_data['name'] = ''
                user_location = user.find_elements_by_xpath(".//*[@class='location']")
                if user_location:
                    user_data['location'] = user_location[0].text
                    num = random.randint(0, len(Keys) - 1)
                    while True:
                        try:
                            print (user_data['location'])
                            geo = geocoder.google(user_data['location'], key=Keys[num])
                            break
                        except Exception as inst:
                            print type(inst)
                            print inst.args
                            print inst
                            del Keys[num]
                            print('-----key invalid')
                    print(geo.json['status'])
                    if geo.json['status'] != "OK":
                        print('-----failed to get geo')
                        user_data['income'] = ''
                        user_data['country'] = ''
                        user_data['state'] = ''
                        user_data['city'] = ''
                        user_data['zipcode'] = ''
                    else:
                        user_data['country'] = geo.country
                        user_data['state'] = geo.state
                        user_data['city'] = geo.city
                        user_data['zipcode'] = geo.postal
                        if user_data['country'] == 'US':
                            try:
                                driver2.get('https://factfinder.census.gov/faces/nav/jsf/pages/community_facts.xhtml')
                                time.sleep(2)
                                try:
                                    driver2.find_element_by_xpath("//*[@class='fsrCloseBtn']").click()
                                except:
                                    print('no x')
                                time.sleep(1)
                                driver2.find_element_by_xpath("//*[@id='cfsearchtextbox']").send_keys(user_data['location'])
                                time.sleep(1)
                                driver2.find_element_by_xpath("//*[@class='autoCompleteGoButton']").click()
                                time.sleep(3)
                                try:
                                    driver2.find_element_by_xpath("//*[@class='fsrCloseBtn']").click()
                                except:
                                    print('no x')
                                buttons = driver2.find_elements_by_xpath("//*[@class='leftnav_btn defined']")
                                for button in buttons:
                                    if button.text == 'Income':
                                        button.click()
                                        break
                                try:
                                    driver2.find_element_by_xpath("//*[@class='fsrCloseBtn']").click()
                                except:
                                    print('no x')
                                time.sleep(2)
                                locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
                                user_data['income'] = locale.atoi(driver2.find_element_by_xpath("//*[@class='value']").text.replace(' ', ''))
                                print (user_data['income'])
                            except Exception as inst:
                                print type(inst)
                                print inst.args
                                print inst
                                print('-----failed to get income')
                                user_data['income'] = ''
                        else:
                            user_data['income'] = ''
                else:
                    user_data['location'] = ''
                    user_data['country'] = ''
                    user_data['state'] = ''
                    user_data['city'] = ''
                    user_data['zipcode'] = ''
                    user_data['income'] = ''
                flag = False
                for level in range(7):
                    if user.find_elements_by_xpath(".//*[@class='levelBadge badge lvl_0" + str(level) + "']"):
                        user_data['level'] = level
                        flag = True
                        break
                if not flag:
                    user_data['level'] = ''
                try:
                    reviews_count = user.find_elements_by_xpath(".//*[@class='reviewerBadge badge']")
                    if reviews_count:
                        reviews_count_str = reviews_count[0].find_element_by_xpath(".//*[@class='badgeText']").text
                        print (reviews_count_str.split())
                        user_data['reviews_count'] = int(reviews_count_str.split()[0])
                    else:
                        user_data['reviews_count'] = ''
                    hotel_reviews = user.find_elements_by_xpath(".//*[@class='contributionReviewBadge badge']")
                    if hotel_reviews:
                        hotel_reviews_str = hotel_reviews[0].find_element_by_xpath(".//*[@class='badgeText']").text
                        print (hotel_reviews_str.split())
                        user_data['hotel_reviews'] = int(hotel_reviews_str.split()[0])
                    else:
                        user_data['hotel_reviews'] = ''
                    helpful_votes = user.find_elements_by_xpath(".//*[@class='helpfulVotesBadge badge']")
                    if helpful_votes:
                        helpful_votes_str = helpful_votes[0].find_element_by_xpath(".//*[@class='badgeText']").text
                        print (helpful_votes_str.split())
                        user_data['helpful_votes'] = int(helpful_votes_str.split()[0])
                    else:
                        user_data['helpful_votes'] = ''
                except Exception as inst:
                    print type(inst)
                    print inst.args
                    print inst
                    print ("-----failed to get badges")
            except Exception as inst:
                print type(inst)
                print inst.args
                print inst
                mark_failed_review(review_id)
                print ("-----failed to retrieve review " + review_id)
                continue
            review_data['user'] = user_data
            with open('./Data/Reviews/' + review_id + '.json', 'w') as f:
                f.write(json.dumps(review_data, indent=4))
    hotel_data['reviews_list'] = reviews_list
    with open('./Data/Hotels/' + hotel_id + '.json', 'w') as f:
        f.write(json.dumps(hotel_data, indent=4))
    time.sleep(6)


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
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver2 = webdriver.Chrome(executable_path='./chromedriver')
    driver3 = webdriver.Chrome(executable_path='./chromedriver')
    for city in cities_list:
        with open('./Data/Cities/' + city[0] + '-' + city[1] + '.txt', 'r') as f:
            hotels_info = json.loads(f.read())
        for hotel_id in hotels_info["hotels_list"]:
            if os.path.exists('./Data/Hotels/' + hotel_id + '.json'):
                continue
            crawl(driver, driver2, driver3, city[1], city[0], hotel_id, 'https://www.tripadvisor.com/Hotel_Review-g' + city[1] + '-d' + hotel_id + '-Reviews')
    driver.quit()
    driver2.quit()
    driver3.quit()
    with open('./Data/cities_failed_list.txt', 'w') as f:
        f.write('\n'.join(failed_list))
    with open('./Data/reviews_failed_list.txt', 'w') as f:
        f.write('\n'.join(failed_review_list))
