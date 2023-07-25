from getToken import *
from signup import *

if __name__ == "__main__":
    android_driver, phone_number = signup()
    web_driver = signin(phone_number)
    signin_code = getCode(android_driver)
    tokens = getAll(web_driver, signin_code)
    print(tokens)

