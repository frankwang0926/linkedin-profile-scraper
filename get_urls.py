# coding: utf-8

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
import pandas as pd
import sys

def get_name_list(df, start_id, end_id):
    name_list = []
    for i in range(start_id - 1, end_id):
        name = df['Name'][i]
        first_name = name.split(", ")[1].split(" ")[0]
        last_name = name.split(", ")[0]
        name_list.append([first_name, last_name])
    return name_list

def get_major_list(df, start_id, end_id):

    major_list = df['Major']
    for i in range(start_id - 1, end_id):
    	major = major_list[i]
    	major = major.rstrip()
    	index = major.find(" - ")
    	if index == -1:
    		major_list.at[i] = major
    	else:
    		major_list.at[i] = major[:index]

    return major_list

def search(driver, search_button, search_string):

	search_button.send_keys(search_string, Keys.RETURN) 
	sleep(3)

	# Try to get the URL
	try:
		url = driver.find_element_by_xpath("//span[@class='entity-result__title-text  t-16']/a").get_attribute('href')
	except:
		url = ""

	search_button.clear()

	print(url)

	return url


def scrape_urls(df, name_list, major_list, user_name, user_password, start_id, end_id):
	# launch
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

	# Enter the search interface by entering a empty string into the search bar
	search_button = driver.find_element_by_class_name("search-global-typeahead__input")
	search_button.send_keys("", Keys.RETURN)
	sleep(5) 

	# Click the all-filters button
	all_filters = driver.find_element_by_css_selector("button[aria-label='All filters']")
	all_filters.click()
	sleep(1) 

	# Use UCLA as a filter
	driver.find_element_by_css_selector("label[for='advanced-filter-schoolFilter-17950']").click() 
	sleep(0.5) 

	# Click the show-results button
	show_results = driver.find_element_by_class_name("search-reusables__secondary-filters-show-results-button")
	show_results.click()
	sleep(5) 

	for i in range(start_id - 1, end_id):

		first_name = name_list[i - (start_id - 1)][0]
		last_name = name_list[i - (start_id - 1)][1]
		major = major_list[i - (start_id - 1)]

		# Enter name and major into the search bar 
		search_query = first_name + " " + last_name + " " + major
		url = search(driver, search_button, search_query)                                     

		if url == "":
			# Get rid of the major part
			search_query = first_name + " " + last_name
			url = search(driver, search_button, search_query)
		else:
			df.at[i, 'Search Query'] = search_query
			df.at[i, 'Code'] = 1
			df.at[i, 'LinkedIn URL'] = url
			continue

		if url == "" and len(last_name.split(" ")) == 1:
			df.at[i, 'LinkedIn URL'] = url
			continue
		elif url == "":
			# Use first_name + the first word of last_name + major
			search_query = first_name + " " + last_name.split(" ")[0] + " " + major
			url = search(driver, search_button, search_query)
		else:
			df.at[i, 'Search Query'] = search_query
			df.at[i, 'Code'] = 2
			df.at[i, 'LinkedIn URL'] = url
			continue

		if url == "":
			# Use first_name + the first word of last_name
			search_query = first_name + " " + last_name.split(" ")[0]
			url = search(driver, search_button, search_query)
		else:
			df.at[i, 'Search Query'] = search_query
			df.at[i, 'Code'] = 3
			df.at[i, 'LinkedIn URL'] = url
			continue

		if url != "":
			df.at[i, 'Search Query'] = search_query
			df.at[i, 'Code'] = 4

		df.at[i, 'LinkedIn URL'] = url
	   
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

	if "Search Query" not in df.columns:
		df["Search Query"] = ""

	if "Code" not in df.columns:
		df["Code"] = ""

	if "LinkedIn URL" not in df.columns:
		df["LinkedIn URL"] = ""

	name_list = get_name_list(df, start_id, end_id)
	major_list = get_major_list(df, start_id, end_id)
	scrape_urls(df, name_list, major_list, user_name, user_password, start_id, end_id)

	df.to_excel('output.xlsx', index=False)


if __name__=="__main__": 
    main() 




