#!/usr/bin/env python2

import sys
import time
import re
import os
import selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
# Open camera ip page
driver.get("http://192.168.1.88/")
actions=ActionChains(driver)

#1
#Center 5
#Left 4
#Right 6
#Up 1
#Down 9

#3
#Sides 1
#Height 2


def main():
	#logn to server
	time.sleep(1)		
	login()
	time.sleep(1)

	#clean panoramic
	os.system("rosservice call /hugin_panorama/reset")

	#ensure to start from one edge
	button=driver.find_element_by_xpath('//*[@id="ytSet2"]/div[1]/div[4]')
	button.click()
	time.sleep(10)
	actions.release(button).perform()
	time.sleep(0.5)

	#store initial image and load new button
	os.system("rosservice call /hugin_panorama/image_saver/save")
	button=driver.find_element_by_xpath('//*[@id="ytSet2"]/div[1]/div[6]')

	#take new 7 pictures
	for i in range (0,7):
		button.click()
		time.sleep(1)
		actions.release(button).perform()
		time.sleep(2.5)
		os.system("rosservice call /hugin_panorama/image_saver/save")

	#stitch images
	os.system("rosservice call /hugin_panorama/stitch")

	#Retrieve image

	
	# Resize scale image
	#min_image_dimension = np.min([self.img.shape[1],self.img.shape[0]])
	#width_percentage = 0.6
    	#width_px = width_percentage*min_image_dimension
    	#scale_img = resize_image(self.scale_img, width_px)

	
def login():
	password=driver.find_element_by_css_selector('#passwd')
	password.send_keys("123qweasd")
	signin=driver.find_element_by_css_selector('#IDS_LGLOGIN')
	signin.click()
	return

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
	
if __name__ == '__main__':
    main()
