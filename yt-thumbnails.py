from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import pickle
import time
import os
import pytesseract
from PIL import Image
from io import BytesIO
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


webdriver_service = Service("./chromedriver-linux64/chromedriver") 

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-infobars") 
chrome_options.add_argument("--disable-extensions")  

driver = webdriver.Chrome(options=chrome_options)

print('initialized')

driver.get("https://www.youtube.com")
driver.save_screenshot('youtube_homepage.png')

time.sleep(5)

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
print(email, password)
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()  # Refresh the page to use the cookies
    print("Cookies loaded and session restored.")
except FileNotFoundError:
    print("Cookies file not found, please log in manually once to save cookies.")

    sign_in_button = driver.find_element(By.XPATH, '//*[@aria-label="Sign in"]')
    print(sign_in_button.text)
    sign_in_button.click()

    time.sleep(5)

    email_field = driver.find_element(By.XPATH, '//input[@type="email"]')
    email_field.send_keys(email)  # Replace with your email
    email_field.send_keys(Keys.ENTER)

    time.sleep(7)

    password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
    # print(type
    password_field.send_keys(str(password))  # Replace with your password
    password_field.send_keys(Keys.ENTER)

    time.sleep(5)
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
time.sleep(5)  # Wait for the recommendations to load
desired_width = 1280
desired_height = 720

if not os.path.exists('thumbnails2'):
    os.makedirs('thumbnails2')

def contains_text(image_data):
    image = Image.open(BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return len(text.strip()) > 0  # If there's any text, return True



def download_images():
    images = driver.find_elements(By.XPATH, '//img[@src]')

    
    for index, img in enumerate(images):
        img_src = img.get_attribute('src')
        # response = requests.get(img_src)

        width = driver.execute_script("return arguments[0].naturalWidth;", img)
        height = driver.execute_script("return arguments[0].naturalHeight;", img)

        if img_src.startswith('https') and width>500:
            response = requests.get(img_src)
            if response.status_code == 200 and contains_text(response.content):
                img_name = os.path.join('downloaded_images', img_src.split('/')[-1])
                date = datetime.today().strftime('%d%m%Y')
                with open(f'thumbnails2/{date}_{index}.jpg', 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {img_name}")
scroll_pause_time = 2  # Pause time to wait for content to load
scroll_limit = 20  # Number of scrolls

try:

    account_menu_button = driver.find_element(By.XPATH, '//button[@aria-label="Account menu"]')
    account_menu_button.click()
    print("Opened account menu.")
except Exception as e:
    print("Could not find or click on the account menu button:", e)

try:
    time.sleep(2)
    menu_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//yt-formatted-string'))
    )
    for item in menu_items:
        print(f"Menu item text: {item.text}")
    
    for item in menu_items:
        if 'Location' in item.text:
            print(f"Found Location option: {item.text}")
            item.click()
            break
except Exception as e:
    print("Could not find or click on the location setting:", e)


try:
    time.sleep(2)
    menu_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//yt-formatted-string'))
    )
    
    for item in menu_items:
        print(f"Menu item text: {item.text}")
    # print('')
    print('Location Menu')
    print('1. United States')
    print('2. Canada')
    print('3. United Kingdom')
    location = int(input("Enter Location number: "))
    if(location <= 3 and location > 0):
        for item in menu_items:
            if ((location ==1 and 'United States' in item.text) or 
                (location ==2 and 'Canada' in item.text) or 
                (location==3 and 'United Kingdom' in item.text)):
                
                print(f"Found Location option: {item.text}")
                item.click()
                break
    else:
        print('Wrong Option, run the code again')
except Exception as e:
    print("Could not select USA as the location:", e)

time.sleep(5)
for _ in range(scroll_limit):
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(scroll_pause_time)  # Wait for new thumbnails to load
    download_images()  # Download images after each scroll
    current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
    # Get the total scrollable height
    total_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
    if(current_scroll_position >= total_scroll_height):
        break

driver.quit()

print("Downloaded all thumbnails successfully!")
