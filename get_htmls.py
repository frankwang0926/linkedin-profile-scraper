# coding: utf-8

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv
import pandas as pd
import math
import sys
import os
import time

# def file_rename(newname, folder_of_download):
#     # time_counter = 0
#     filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
#     # while '.crdownload' in filename:
#     #     time.sleep(1)
#     #     time_counter += 1
#     #     if time_counter > time_to_wait:
#     #         raise Exception('Waited too long for file to download')
#     # filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
#     os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))

def get_htmls(urls, user_name, user_password, start_id, end_id):
	# launch Chrome
	driver = webdriver.Chrome(ChromeDriverManager().install())

	# enter the LinkedIn website
	driver.get('https://www.linkedin.com') 

	# Click the sign-in button
	sign_in_button = driver.find_element_by_class_name('nav__button-secondary')
	sign_in_button.click()
	sleep(0.5)                          

	# Enter username
	username = driver.find_element_by_name('session_key')                   
	username.send_keys(user_name)
	sleep(0.5)                           

	# Enter password
	password = driver.find_element_by_name('session_password')              
	password.send_keys(user_password) 
	sleep(0.5)                                   

	# Click the log-in button
	log_in_button = driver.find_element_by_class_name('btn__primary--large')                                                                   
	log_in_button.click() 
	sleep(0.5)   

	timeout = 10

	for i in range(start_id - 1, end_id):

		url = urls[i]

		if pd.isna(url):
			continue

		driver.get(url)
		sleep(2)

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(4)

		try:
		    element_present = EC.presence_of_element_located((By.XPATH, "//section[@class='pv-profile-section pv-interests-section artdeco-card mt4 p5 ember-view']/h2"))
		    WebDriverWait(driver, timeout).until(element_present)
		except TimeoutException:
		    print("Timed out waiting for page to load [{}]".format(i))
		finally:
		    print("Page loaded [{}]".format(i))

		html = driver.page_source

		f = open(str(i) + ".html", "w")

		f.write(html)

		f.close()
  
	# Terminate the application
	driver.quit()


def main(): 

	if len(sys.argv) != 6:
		sys.exit("ERROR: Wrong Number of Arguments")

	user_name = sys.argv[1]
	user_password = sys.argv[2]
	start_id = int(sys.argv[3])
	end_id = int(sys.argv[4])
	input_file = sys.argv[5]

	df = pd.read_excel(input_file)

	urls = df["LinkedIn URL"]

	get_htmls(urls, user_name, user_password, start_id, end_id)


if __name__=="__main__": 
    main() 










