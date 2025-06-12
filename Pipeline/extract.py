from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

# function to wait 10 second for single element
def wait_single(driver, selector):
  try: 
    return WebDriverWait(driver, 10).until(
      EC.visibility_of_element_located(
        (
          By.CSS_SELECTOR,
          selector
        )
      )
    )
  except Exception as e:
    print(f"you have error: {e}")

# function to wait 10 second for multiple elements (returns a list)
def wait_multiple(driver, selector):
  try: 
    return WebDriverWait(driver, 10).until(
      EC.visibility_of_all_elements_located(
        (
          By.CSS_SELECTOR,
          selector
        )
      )
  )
  except Exception as e:
    print(f"you have error: {e}")

# for bs4
def get_text_single(page, selector):
  elem = page.select_one(selector)
  if elem:
    return elem.get_text()
  return ''

def scrollBottom(driver):

  last_height = driver.execute_script("return document.body.scrollHeight")

  while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load page
    time.sleep(2)
    
    # Calculate new scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        return False  # No more content
    last_height = new_height

def getHotelData(url, price='Unkown', keyword='Unkown'):

  # make request to page
  page = requests.get(url)
  page = BeautifulSoup(page.content)

  # get useful data
  title = get_text_single(page, 'h2')

  address_elem = page.select_one('#map_trigger_header_pin')
  address = ''
  if address_elem:
    l = address_elem.get_attribute_list('data-atlas-latlng')
    if len(l) > 0:
      address = l[0]

  description = get_text_single(page, '[data-testid="property-description"]')

  address2 = get_text_single(page, 
    '[data-testid="PropertyHeaderAddressDesktop-wrapper"] div div span button div'
  )

  reviews_cnt = get_text_single(page, 
    '[data-testid="review-score-right-component"] div div:nth-child(2)'
  )

  avg_rating = get_text_single(page, 
    '[data-testid="review-score-right-component"] div div:nth-child(1)'
  )

  # collect faclilities ##########################################
  facilities = []
  facility_container = page.select(
    '[data-testid="property-most-popular-facilities-wrapper"] div ul li'
  )

  for elem in facility_container:
    text = get_text_single(elem,
      'div div div span div span'
    )
    facilities.append(text)
  # end of faclilities ############################################

  # collect rating details ##############################################
  rating = dict()
  ratings = page.select(
    '[data-testid="review-subscore"]'
  )

  for elem in ratings:
    metric = get_text_single(elem, 
      '[data-testid="review-subscore"] div div div:nth-child(1) div span'
    )

    val = get_text_single(elem, 
      '[data-testid="review-subscore"] div div div:nth-child(2) div'
    )
    
    rating[metric] = val
  #######################################################################


  # comments ####################################################
  comments = []
  li = page.select('[aria-label="Guests who stayed here loved"] li')

  for child in li:
    name = get_text_single(child, 'div div div:nth-child(1) div div:nth-child(2) div:nth-child(1)')
    country = get_text_single(child, 'div div div:nth-child(1) div div:nth-child(2) div:nth-child(2) span')
    desc = get_text_single(child, 'div div div:nth-child(2) div div span:nth-child(2)')

    comments.append({
      'name': name,
      'country': country,
      'description': desc
    })
  ###############################################################
  
  return {
    'title': title,
    'url': url,
    'price': price,
    'address': address,
    'description': description,
    'address2': address2,
    'facilities': facilities,
    'reviews_cnt': reviews_cnt,
    "rating": avg_rating,
    'rating_details': rating,
    'comments': comments,
    'city': keyword
  }

def extract(keyword='', threshold=100, loads=5):

  # init the driver
  print("initialize driver...")
  options = Options()
  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
  driver = webdriver.Chrome(options=options)

  # to behave like a human
  stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        fix_hairline=True
        )
  
  # opens the link in our opened tap
  driver.get("https://www.booking.com")
  print("driver initialized successfully")

  print(f"Typing keyword {keyword} in the input field")
  # search form
  form = wait_single(driver, 'form[aria-label="Search properties"]')

  # button is not visible when the input is empty
  # clearBtn = wait_single(driver, 'form[aria-label="Search properties"] button[type="button"]')

  # input element
  inputElem = wait_single(driver, 'input[aria-label="Where are you going?"]')
  inputElem.send_keys(keyword)

  # to wait untill search autocomplete fileds is set properly
  print("Waiting for auto complete search...")
  try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#autocomplete-result-0 div div div div"), "Alexandria"))
  except Exception as e:
    print(f"auto complete faild (You are using wrong keyword)")
    # stop the function
    return []
  
  form.submit()
  print("Form submitted")

  # load more content
  i = 0
  while(i < max(loads, 0)):
    print(f"Scrolling down {i}...")
    scrollBottom(driver)
    loadMore = driver.find_element(By.XPATH, "//button[span[text()='Load more results']]")
    loadMore.click()
    i += 1

  a = wait_multiple(driver, '[data-results-container="1"] [data-testid="property-card"] a')
  # price = wait_multiple(driver, '[data-results-container="1"] [data-testid="price-and-discounted-price"]')
  print(f"{len(a)} hotels found !!")
  
  # apply our threshold
  a = a[:threshold]
  print(f"Scrapping first {min(threshold, len(a))} hotels...")

  # scrap each single hotel
  st = set()
  allData = []
  for i in range(len(a)):
    print(f"Scrapping hotel {i}...")
    url = a[i].get_attribute('href')
    # price = price[i].text if i < len(price) else "Unkown"
    
    if(url in st):
      print(f"Hotel {i} is duplicated !")
      continue

    st.add(url)
    # scrap with bs4
    data = getHotelData(url, keyword=keyword)
    allData.append(data)
    print(f"Hotel {i} successfully scrapped")

  driver.quit()
  print("Driver closed successfully")
  print(f"{len(allData)} hotels successfully scrapped !")
  return allData