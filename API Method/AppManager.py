from signup import signup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def extractLoginCode(msg):
    # Split the message into a list of words
    words = msg.split()

    # Find the index of the word "code:"
    code_index = words.index("code:")

    # Extract the login code itself
    login_code = words[code_index+1]

    return login_code


def updateApp():
    android_driver, number = signup()
    driver = webdriver.Chrome()

    wait = WebDriverWait(driver, 10)
    android_wait = WebDriverWait(android_driver, 10)

    # Go to the Google home page
    driver.get("https://my.telegram.org/auth")
    phone = wait.until(EC.visibility_of_element_located((By.ID, 'my_login_phone')))
    phone.send_keys(number)

    next = driver.find_element(By.TAG_NAME, 'button')
    next.click()
    
    confirm = android_wait.until(EC.visibility_of_element_located((By.ID, 'my_password')))
    
    # extract confirm code
    tg = android_driver.find_element(By.CLASS_NAME, 'android.view.ViewGroup')
    tg.click()

    msg = android_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'android.view.ViewGroup')))
    code = extractLoginCode(msg[-1].text)
    confirm.send_keys(code)

    sign = driver.find_elements(By.TAG_NAME, 'button')
    sign[1].click()

    driver.get('https://my.telegram.org/apps')
    app_title = wait.until(EC.visibility_of_element_located((By.ID, 'app_title')))
    app_title.send_keys('auto bot generation')

    app_shortname = wait.until(EC.visibility_of_element_located((By.ID, 'app_shortname')))
    app_shortname.send_keys('bot mum')

    app_url = wait.until(EC.visibility_of_element_located((By.ID, 'app_url')))
    app_url.send_keys('https://web.telegram.org/')

    save = driver.find_element(By.TAG_NAME, 'button')
    save.click()

    api_id = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'span')))
    api_id = api_id.text

    api_hash = driver.find_elements('span')[2].text
    
    driver.quit()
    return phone, api_id, api_hash

