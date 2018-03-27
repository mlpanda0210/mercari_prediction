import sys
import os
from selenium import webdriver
import pandas as pd
import time

class SearchMercariData(object):
    def __init__(self,input_data):
        self.input_data = input_data
        self.num_page = 1

    def search_from_sold_list(self):
        df_url = self.get_url(self.num_page)
        df = self.get_details(df_url)
        return df

    def get_url(self, num_page):
        browser = webdriver.Chrome()
        browser.get("https://www.mercari.com/jp/search/?keyword=")
        browser.find_element_by_xpath("/html/body/div/main/div[2]/form/div[2]/div[8]/div/div[2]/label").click()
        browser.find_element_by_xpath("/html/body/div/main/div[2]/form/div[2]/div[10]/button").click()
        df = pd.DataFrame()
        page=0
        for i in range(num_page):
            if len(browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
                print("######################page: {} ########################".format(page))
                print("Starting to get posts...")
                posts = browser.find_elements_by_css_selector(".items-box")
                for post in posts:
                    url = post.find_element_by_css_selector("a").get_attribute("href")
                    box_photo = post.find_element_by_css_selector(".items-box-photo")
                    pic = box_photo.find_element_by_css_selector("img").get_attribute("data-src")
                    se = pd.Series([url,pic],index=['url','pic'])
                    df = df.append(se, ignore_index=True)
                page+=1

                btn = browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
                print("next url:{}".format(btn))

                df = df.drop_duplicates()
                browser.get(btn)
                print("Moving to next page......")
            else:
                print("no pager exist anymore")
        return df


    def get_details(self,df_sold_out):
        df_details_list = pd.DataFrame()
        browser = webdriver.Chrome()
        for i in range(df_sold_out.shape[0]):
            url  = df_sold_out["url"].values[i]
            pic  = df_sold_out["pic"].values[i]
            browser.get(url)
            try:
                item_name =browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/h2").text
                try:
                    sold_badge =browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[1]/div/div[2]/div").text
                except:
                    sold_badge = "NOT_SOLD"
                main_category =browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[1]/table/tbody/tr[2]/td/a[1]/div").text
                sub1_category =browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[1]/table/tbody/tr[2]/td/a[2]/div").text
                sub2_category = browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[1]/table/tbody/tr[2]/td/a[3]/div").text
                brand_name = browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[1]/table/tbody/tr[3]/td").text

                box_details = browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[1]/table").text
                list_item_condition = ["新品、未使用","未使用に近い","目立った傷や汚れなし","やや傷や汚れあり","傷や汚れあり"]
                box_details = box_details.replace("\n"," ").split(" ")

                for word in list_item_condition:
                    try:
                        item_condition = box_details[box_details.index(word)]
                        break
                    except:
                        next
                shipping_fee =  browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[2]/span[3]").text
                item_description= browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[3]").text
                price = browser.find_element_by_xpath("/html/body/div[1]/main/div[1]/section[1]/div[2]/span[1]").text

                item_description = item_description.replace("\n"," ")
                price = price.replace("¥ ","")
                se = pd.Series([item_name, sold_badge, main_category,sub1_category,sub2_category,brand_name,item_condition,shipping_fee,item_description,price,url,pic],
                                   ["item_name", "sold_badge","main_category","sub1_category","sub2_category","brand_name","item_condition","shipping_fee","item_description","price","url","pic"])
                df_details_list = df_details_list.append(se, ignore_index=True)
                print("{} details of {} was added".format(i,url) )
            except:
                print("{} are not found".format(url))
        return df_details_list
