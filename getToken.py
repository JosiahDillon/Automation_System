############################################################
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from time import sleep
import random
import string
import pyotp
###########################################################

qr_code_hash = "lruzgenpayp55icmf6dypdcw"
stripe_email = "pottercarlos068@gmail.com"
stripe_password = "P!_kMPz?zV-KN2^"

####################################################
def generate_bot_name():
    # Set the length of the random character part of the name
    name_length = 8
    
    # Generate a random string of characters
    random_chars = ''.join(random.choices(string.ascii_letters, k=name_length))
    
    # Generate a random number
    number = random.randint(0, 999)
    
    # Combine the random characters and number to form the bot name
    bot_name = random_chars + str(number)
    
    return bot_name


####################################################
def debug():
    cmd = input('>>>')
    try:
        if cmd=='exit':
            print('<<<exited!')
        else:
            exec(cmd)
            print("------------------success")
            debug()
    except:
        print("__________________failed, error")
        debug()
        pass

##############################################################
def waitInfinite(callback, debug = False):
    sleep(0.3)
    yet = True
    while yet:
        try:
            callback()
            yet = False
        except NoSuchElementException:
            pass
        except JavascriptException: 
            pass
        except StaleElementReferenceException:
            pass
def waitUntil(callback, driver, selector):
    sleep(0.3)
    yet = True
    while yet:
        try:
            callback(driver.find_element(By.CSS_SELECTOR, selector))
            yet = False
        except:
            pass

############################################################

def waitUntil1(callback, driver, selector):
    sleep(0.5)
    yet = True
    while yet:
        try:
            callback(driver.find_elements(By.CSS_SELECTOR, selector)[1])
            yet = False
        except Exception as e:
            sleep(0.1)
            pass

############################################################

def real_click_button(driver, button_name):
    sleep(2)
    print("click_button function calling...", button_name, " selected")
    buttons = driver.find_elements(By.XPATH, "//button")
    select_button = None
    for button in buttons:
        if button_name == button.text:
            select_button = button
    print('select_button,    ', select_button)
    if select_button is not None:
        select_button.click()

########################################################

def Validate_force(callback, debug=False):
    while True:
        sleep(0.5)
        try:
            callback()
            break
        except:
            pass
########################################################

def click_button(driver, button_name):
    waitInfinite(lambda: real_click_button(driver, button_name))

    
########################################################

def signin(phone_number):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    waitInfinite(lambda: driver.get("https://web.telegram.org/a/"))
    sleep(10)
    print('here')
    click_button(driver, "LOG IN BY PHONE NUMBER")

    sleep(4)
    driver.find_element(By.ID, 'sign-in-phone-number').send_keys(Keys.BACKSPACE)
    driver.find_element(By.ID, 'sign-in-phone-number').send_keys(Keys.BACKSPACE)
    driver.find_element(By.ID, 'sign-in-phone-number').send_keys(Keys.BACKSPACE)
    driver.find_element(By.ID, 'sign-in-phone-number').send_keys(Keys.BACKSPACE)
    driver.find_element(By.ID, "sign-in-phone-number").send_keys(phone_number)
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    sleep(0.5)
    return driver

def getAll(driver, activity_code):
    driver.find_element(By.ID, 'sign-in-code').send_keys(activity_code)
    sleep(2)
    result = []
    for i in range(10):
        print('here is ', i)
        botname = generate_bot_name()
        botname_t = botname+'_bot'
        try:
            driver.find_element(By.ID, 'telegram-search-input').send_keys('BotFather')
            sleep(2)
            driver.find_element(By.ID, 'telegram-search-input').send_keys(Keys.ENTER)
            sleep(1)
            click_button(driver, "START")
            Validate_force(lambda: (
                driver.find_element(By.ID, "editable-message-text").send_keys('/newbot'),
                driver.find_element(By.ID, "editable-message-text").send_keys(Keys.ENTER)
                )
            )
            Validate_force(lambda: (
                driver.find_element(By.ID, "editable-message-text").send_keys(botname),
                driver.find_element(By.ID, "editable-message-text").send_keys(Keys.ENTER)
                )
            )
            Validate_force(lambda: (
                driver.find_element(By.ID, "editable-message-text").send_keys(botname_t),
                driver.find_element(By.ID, "editable-message-text").send_keys(Keys.ENTER)
                )
            )
            Validate_force(lambda: (
                driver.find_element(By.ID, "editable-message-text").send_keys('/mybots'),
                driver.find_element(By.ID, "editable-message-text").send_keys(Keys.ENTER)
                )
            )
            click_button(driver, "@"+botname_t)
            driver.refresh()
            sleep(7)
            click_button(driver, "Payments")
            driver.refresh()
            sleep(7)
            click_button(driver, '»')
            driver.refresh()
            sleep(7)
            click_button(driver, 'Stripe »')
            driver.refresh()
            sleep(7)
            click_button(driver, 'Connect Stripe Live')
            click_button(driver, 'Authorize')
            click_button(driver, 'OPEN LINK')
            handles = driver.window_handles
            driver.switch_to.window(handles[1])
            driver.find_element(By.ID, "email").send_keys(stripe_email)
            click_button(driver, "Continue")
            driver.find_element(By.ID, "password").send_keys(stripe_password)
            click_button(driver, "Log in")
            totp = pyotp.TOTP(qr_code_hash)
            otp = totp.now()
            driver.find_element(By.CSS_SELECTOR, 'input[type="tel"]').send_keys(otp)
            click_button(driver, "Connect")
            driver.switch_to.window(handles[0])
            driver.find_element(By.ID, 'telegram-search-input').send_keys('BotFather')
            sleep(2)
            driver.find_element(By.ID, 'telegram-search-input').send_keys(Keys.ENTER)
            bot_token = driver.find_elements(By.CSS_SELECTOR, "code")[0].text
            provider_token = driver.find_elements(By.CSS_SELECTOR, "code")[1].text
            driver.find_element(By.CSS_SELECTOR, "button[title='More actions']").click()
            driver.find_element(By.CSS_SELECTOR, "i.icon.icon-delete").click()
            click_button(driver, "DELETE")
            driver.find_element(By.ID, 'telegram-search-input').send_keys('Stripe Bot')
            sleep(2)
            driver.find_element(By.ID, 'telegram-search-input').send_keys(Keys.ENTER)
            bot_token = driver.find_elements(By.CSS_SELECTOR, "code")[0].text
            provider_token = driver.find_elements(By.CSS_SELECTOR, "code")[1].text
            driver.find_element(By.CSS_SELECTOR, "button[title='More actions']").click()
            driver.find_element(By.CSS_SELECTOR, "i.icon.icon-delete").click()
            click_button(driver, "DELETE")
            result.append([botname_t, bot_token, provider_token])
        except Exception as e:
            print(e)
    return result
