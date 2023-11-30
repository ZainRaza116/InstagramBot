
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
import pandas as pd
from selenium.webdriver.common.keys import Keys

def login_to_instagram():
    df = pd.read_csv('LOGIN_SET.csv')
    if 'email' not in df or 'password' not in df:
        print("The Excel sheet must contain 'email' and 'password' columns.")
        return
    login = df.at[0, 'email']
    password = df.at[0, 'password']

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.instagram.com/")
        # Use WebDriverWait to wait for elements
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='_aa4b _add6 _ac4d _ap35']"))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Password']"))
        )

        # Enter your login credentials
        username.send_keys(login)
        password_input.send_keys(password)

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1e56ztr x540dpk x1m39q7l x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]'))
        )
        button.click()

        print('Entering into the IG')
        time.sleep(10)
        driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(10)
        messages = driver.find_elements(By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np']")
        driver.execute_script("window.open('', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        login1 = df.at[1, 'email']
        password1 = df.at[1, 'password']
        driver.get("https://youai.ai/login")
        time.sleep(5)
        email_address = driver.find_elements(By.XPATH, '//button[@class="sc-60a7ef6f-1 xUzlo"][1]')
        email_address[0].click()
        time.sleep(4)

        email_bot = driver.find_elements(By.XPATH, "//input[@placeholder='name@example.com']")
        password_bot = driver.find_elements(By.XPATH, '//input[@placeholder="••••••••••"]')

        email_bot[0].send_keys(login1)
        password_bot[0].send_keys(password1)

        email_address = driver.find_elements(By.XPATH, '//button[@class="sc-60a7ef6f-1 xUzlo"]')
        email_address[0].click()

        time.sleep(10)
        driver.get(
            "https://youai.ai/ais/2f9a6d39-6858-4422-b0dc-143c69c70136/use?draftVersionId=1fea6731-db9a-467e-ac51-3bd34055f3b9")
        time.sleep(2)
        bot = driver.find_elements(By.XPATH, "//textarea[@placeholder='Write something...']")
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        for i in messages:
            i.click()
            time.sleep(5)
            text = driver.find_elements(By.XPATH, "//div[@class='x78zum5 xh8yej3']")
            if text:
                last_message_element = text[-1].text
                print("Last message text:", last_message_element)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(5)
                for element in bot:
                    element.send_keys(last_message_element)
                    element.send_keys(Keys.RETURN)
                    break
                time.sleep(60)
                copied = driver.find_elements(By.XPATH, '(//div[@class="sc-c4d9e300-0 eDJZhp __explicit-message"])')[-1]
                copied_text = copied.text
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(5)
                contenteditable_div = driver.find_element(By.XPATH,'//div[@aria-label="Message"]')
                contenteditable_div.click()
                contenteditable_div.send_keys(copied_text)
                time.sleep(10)
                driver.execute_script("arguments[0].innerHTML = arguments[1]", contenteditable_div, copied_text)

    except NoSuchElementException as e:
        print(f"Element not found: {e}")

    finally:
        print("Done")
        driver.quit()
