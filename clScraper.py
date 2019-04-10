import time
from selenium import webdriver
import csv

#setup driver for Chrome
def initialize_driver():
  options = webdriver.ChromeOptions()
  # prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
  # options.add_experimental_option('prefs', prefs)

  #specifies that browser will be headless
  options.add_argument('headless')

  driver = webdriver.Chrome(chrome_options=options)
  return driver

#seeks list of all relevant CL locations close by (on righthand side)
#must get a starting point as input
def find_surrounding_loc(start_point):
  driver.get(f'https://{start_point}.craigslist.org')
  locations = []
  locations.append(start_point)
  where = driver.find_elements_by_class_name('s')
  for place in where:
    location= place.find_element_by_xpath('.//a')
    if location.text:
      locations.append(location.text)

  return locations

#function that searches each page and assigns to csv
#all output is appended to csv
def search(search_loc):
  # driver = webdriver.Chrome('/usr/bin/chromedriver')
  driver.get(f'http://{search_loc}.craigslist.org/d/free-stuff/search/zip')
  where = driver.find_elements_by_class_name('rows')

  #can't say I understand why I had to write this as a loop
  for item in where:
    item = item.find_elements_by_css_selector('li.result-row')

  for i in item:
    try:

      item_title = i.find_element_by_css_selector('a.result-title')
      title = item_title.text

      item_details_link= item_title.get_attribute("href")
      link = item_details_link




      item_post_date = i.find_element_by_css_selector('time.result-date')
      date = item_post_date.get_attribute("datetime")

      item_loc = i.find_element_by_css_selector('span.result-hood')
      place = item_loc.text

      #search link for item details
      desc = expand_desc(item_details_link)

      #write output to csv
      write_to_csv(title, date, place, desc, link)
    except:
      continue



#clicks on each item's link for inner details
def expand_desc(url):
  print(url)

  #initializing a new driver could be the reason we're slowing down
  explorer = initialize_driver()
  try:
    explorer.get(url)
    body = explorer.find_elements_by_css_selector('section #postingbody')
    body = body[0].text
    explorer.quit()
    print(body)
    return body
  except:
    print('in error handling')
    explorer.quit()
    return 'error'

#writes data to csv file
def write_to_csv(title, date, place, desc, link):
  with open('search_results.csv', mode='a') as result_row:
    result_row = csv.writer(result_row, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    result_row.writerow([title, date, place, desc, link])

#joins all place names with two or more words
#ex 'new jersey' => 'newjersey'
def join_multi_word_names(place_name):
  place_name = place_name.split()
  return "".join(place_name)



#main thread
starting_point = join_multi_word_names(input("where should we begin our search? - please enter a place name - "))
driver = initialize_driver()
places_to_search = find_surrounding_loc(starting_point)
print(places_to_search)

for place in places_to_search:
  search(place)

driver.quit()


