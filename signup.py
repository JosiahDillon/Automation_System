from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import requests
import json
import os

# SMS config
API_KEY = 'Y3RI_fbBnETtQW3RPq-JNC90EMEFSG9G'
country_id = 5
application_id = 3

# Appium server
server = 'http://127.0.0.1:4723/wd/hub'

apk = os.path.join(os.getcwd(), 'Telegram.apk')
# Set up Appium capabilities for your device or emulator
desired_caps = {
    "platformName": "Android",
    "platformVersion": "11",
    "deviceName": "cloud",
    "appPackage": "org.telegram.messenger",
    "appActivity": "org.telegram.ui.LaunchActivity",
    "app": apk
}

# New phone number
def getNumber():
    response = requests.get(f'http://api.sms-man.com/control/get-number?token={API_KEY}&country_id={country_id}&application_id={application_id}')
    data = response.content
    json_data = json.loads(data)
    return json_data

# Receive SMS
def getSMS(request_id):
    response = requests.get(f'http://api.sms-man.com/control/get-sms?token={API_KEY}&request_id={request_id}')
    data_r = response.content
    json_data_r = json.loads(data_r)
    print(json_data_r)
    sms = json_data_r['sms_code']
    return sms

# random name
def generate_username():
    # Generate a random username with a length between 4 and 8 characters
    length = random.randint(6, 8)
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return username

# Extract Login code
def extractLoginCode(msg):
    # Split the message into a list of words
    words = msg.split()

    # Find the index of the word "code:"
    code_index = words.index("code:")

    # Extract the login code itself
    login_code = words[code_index+1]

    return login_code

# Sign up => return phone
def signup():
    
    # Launch the Telegram app
    
    android_driver = webdriver.Remote(server, desired_caps)

    wait = WebDriverWait(android_driver, 20)
    
    # handle notification alert
    alert = wait.until(EC.alert_is_present())
    alert.accept()

    # Navigate to the signup screen
    start_btn = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.widget.TextView')))
    start_btn[-1].click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.widget.ImageView')))
    continue_btn = android_driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
    continue_btn[-1].click()

    # handle notification alert
    alert = wait.until(EC.alert_is_present())
    alert.dismiss()

    phone = wait.until(EC.visibility_of_element_located((By.XPATH, '//android.widget.EditText[@content-desc="Country code"]')))
    
    for i in range(10):
        data = getNumber()
        phone.send_keys(data['number'])
        
        next = android_driver.find_element(By.XPATH, '//android.widget.FrameLayout[@content-desc="Done"]/android.view.View')
        next.click()
        
        next = wait.until(EC.visibility_of_element_located((By.XPATH, '//android.widget.FrameLayout[@content-desc="Done"]')))
        next.click()


        if i == 0:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.widget.ImageView')))
            continue_btn = android_driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
            continue_btn[-1].click()
            # handle notification alert
            alert = wait.until(EC.alert_is_present())
            alert.accept()
            
            # handle notification alert
            alert = wait.until(EC.alert_is_present())
            alert.accept()
        
        
        try:
            while True:
                check = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.widget.TextView')))
                if check.text != 'Your phone number':
                    break
            
            print(check.text)
            
            if 'Check your Telegram messages' == check.text:
                code = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.widget.EditText')))
                sms = getSMS(data['request_id'])
                code.send_keys(sms)
                
                next = wait.until(EC.visibility_of_element_located((By.XPATH, '//android.widget.FrameLayout[@content-desc="Done"]/android.view.View')))
                name = wait.until(EC.visibility_of_element_located((By.XPATH, 'android.widget.EditText')))
                name.send_keys(generate_username)
                
                next.click()
                
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.widget.ImageView')))
                continue_btn = android_driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
                continue_btn[-1].click()
                
                # 
                # handle notification alert
                
                return android_driver, data['number']
            else:
                ps = wait.until(EC.visibility_of_all_element_located((By.CLASS_NAME, 'android.view.ViewGroup')))
                ps.click()
                ph = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.widget.EditText')))
                ph[0].clear()
                ph[1].clear()
        except Exception as e:
            back = wait.until(EC.visibility_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="Back"]')))
            back.click()
            edit = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.widget.TextView')))
            edit[2].click()
            ph = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'android.widget.EditText')))
            ph[0].clear()
            ph[1].clear()
    
    return False
    
def getCode(driver):
    wait = WebDriverWait(driver, 20)
    alert = wait.until(EC.alert_is_present())
    alert.accept()
    tg_gp = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.view.ViewGroup')))
    tg_gp.click()
    
    msg = wait.until(EC.visibility_of_elements_located((By.CLASS_NAME, 'android.view.ViewGroup')))
    driver.quit()
    return extractLoginCode(msg[-1].text)


if __name__ == "__main__":
    signup()