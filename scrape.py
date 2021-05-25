# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup

def clean(input_string):

	temp_list = input_string.split('\n')
	temp_list = [x.strip() for x in temp_list if x.strip() != '']

	return temp_list

# Experience case 1
def add_experience_1(df, i, exp_list, exp_index):

	df.at[i, '[Exp ' + str(exp_index) + '] Title'] = exp_list[0]

	for j in range(len(exp_list)):
		if exp_list[j] == "Company Name":
			df.at[i, '[Exp ' + str(exp_index) + '] Company Name'] = exp_list[j+1]
		elif exp_list[j] == "Dates Employed":
			df.at[i, '[Exp ' + str(exp_index) + '] Dates Employed'] = exp_list[j+1]
		elif exp_list[j] == "Location":
			df.at[i, '[Exp ' + str(exp_index) + '] Location'] = exp_list[j+1]

# Experience case 2
def add_experience_2(df, i, exp_list, exp_index):

	title_string = ""
	dates_string = ""
	location_string = ""

	for j in range(len(exp_list)):
		if exp_list[j] == "Company Name":
			df.at[i, '[Exp ' + str(exp_index) + '] Company Name'] = exp_list[j+1]
		elif exp_list[j] == "Title":
			title_string += (exp_list[j+1] + '\r\n')
		elif exp_list[j] == "Dates Employed":
			dates_string += (exp_list[j+1] + '\r\n')
		elif exp_list[j] == "Location":
			location_string += (exp_list[j+1] + '\r\n')
	
	df.at[i, '[Exp ' + str(exp_index) + '] Title'] = title_string[:-2]
	df.at[i, '[Exp ' + str(exp_index) + '] Dates Employed'] = dates_string[:-2]
	df.at[i, '[Exp ' + str(exp_index) + '] Location'] = location_string[:-2]

def add_experience(df, i, exp_list, exp_index):
	if exp_list[0] != "Company Name":
		add_experience_1(df, i, exp_list, exp_index)
	else:
		add_experience_2(df, i, exp_list, exp_index)

def add_education(df, i, edu_list, edu_index):

	df.at[i, '[Edu ' + str(edu_index) + '] School'] = edu_list[0]

	for j in range(len(edu_list)):
		if edu_list[j] == "Degree Name":
			df.at[i, '[Edu ' + str(edu_index) + '] Degree Name'] = edu_list[j+1]
		elif edu_list[j] == "Field Of Study":
			df.at[i, '[Edu ' + str(edu_index) + '] Field Of Study'] = edu_list[j+1]
		elif edu_list[j] == "Dates attended or expected graduation":
			df.at[i, '[Edu ' + str(edu_index) + '] Dates attended or expected graduation'] = edu_list[j+1]

def scrape_data(df):

	for i in range(len(df.index)):

		file_name = "HTMLs/" + str(i) + ".html"

		try:
			with open(file_name) as fp:
				soup = BeautifulSoup(fp, "html.parser")
		except:
			continue

	    # get the title
		try:
			title = soup.find("h2", class_="mt1 t-18 t-black t-normal break-words").text.strip()
		except:
			title = ""

		df.at[i, 'Title'] = title

	    # get the location
		try:
			location = soup.find("li", class_="t-16 t-black t-normal inline-block").text.strip()
		except:
			location = ""

		df.at[i, 'Location'] = location

	    # get the experiences
		exps = soup.find_all("li", class_="pv-entity__position-group-pager pv-profile-section__list-item ember-view")

		if len(exps) > 5:
			exps = exps[0:5]

		for j in range(len(exps)):
			exp_list = clean(exps[j].text)
			add_experience(df, i, exp_list, j+1)

		# get the educations
		edus = soup.find_all("li", class_="pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view")

		if len(edus) > 3:
			edus = edus[0:3]

		for j in range(len(edus)):
			edu_list = clean(edus[j].text)
			add_education(df, i, edu_list, j+1)

		soup.decompose()
		fp.close()


def main(): 

	df = pd.read_excel("input.xlsx")
	df["Title"] = ""
	df["Location"] = ""

	for i in range(1, 6):
		df["[Exp " + str(i) + "] Title"] = ""
		df["[Exp " + str(i) + "] Company Name"] = ""
		df["[Exp " + str(i) + "] Dates Employed"] = ""
		df["[Exp " + str(i) + "] Location"] = ""

	for i in range(1, 4):
		df["[Edu " + str(i) + "] School"] = ""
		df["[Edu " + str(i) + "] Degree Name"] = ""
		df["[Edu " + str(i) + "] Field Of Study"] = ""
		df["[Edu " + str(i) + "] Dates attended or expected graduation"] = ""

	scrape_data(df)

	df.to_excel('output.xlsx', index=False)


if __name__=="__main__": 
    main() 








