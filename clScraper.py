import time
from selenium import webdriver

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
def find_surrounding_loc():
  driver.get('https://www.craigslist.org')
  locations = []
  where = driver.find_elements_by_class_name('s')
  for place in where:
    location= place.find_element_by_xpath('.//a')
    if location.text:
      persons.append({'location': location.text})
  return locations

def search(search_loc):
  # driver = webdriver.Chrome('/usr/bin/chromedriver')
  driver.get(f'http://{search_loc}.craigslist.org/d/free-stuff/search/zip')
  items = []
  where = driver.find_elements_by_class_name('rows')
  item = None
  for item in where:
    item = item.find_elements_by_css_selector('li.result-row')

  for i in item:
    item_obj = {}
    try:

      item_title = i.find_element_by_css_selector('a.result-title')
      item_obj['title'] = item_title.text

      item_details_link= item_title.get_attribute("href")
      item_obj['link'] = item_details_link

      #search link for item details
      item_obj['desc'] = expand_desc(item_details_link)


      item_post_date = i.find_element_by_css_selector('time.result-date')
      item_obj['date'] = item_post_date.get_attribute("datetime")

      item_loc = i.find_element_by_css_selector('span.result-hood')
      item_obj['location'] = item_loc.text
    except:
      continue

    items.append(item_obj)
  return items

#crawl each item's link for details
def expand_desc(url):
  print(url)
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

#main thread
driver = initialize_driver()
res = search('newjersey')
#res = expand_desc('https://newjersey.craigslist.org/zip/d/stockholm-corner-bathtub-free/6840756927.html')
print(res)
driver.quit()


