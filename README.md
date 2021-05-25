# linkedin-profile-scraper

Note: the data collected by this tool is only used for data analysis and is publicly available online

libraries used: selenium, BeautifulSoup, pandas

### get_urls.py
Given a list of student names and majors, scrape their LinkedIn URLs

### get_htmls.py
Given a list of LinkedIn URLs, scrape the corresponding HTML pages

### scrape.py
1. Scrape key information such as title, company name, school, and field of study from a set of HTML pages
2. Generate a well-formatted excel sheet at the end
