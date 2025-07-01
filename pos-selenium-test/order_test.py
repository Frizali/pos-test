import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time

# ---------------------------------------- Initialize ---------------------------------------- 
url = "http://localhost:5101/auth/login"

# User
username = "Fahrizal Ali"
password = "Rizal@292021173"

driver = webdriver.Edge()

def generate_log(testName, status):
    with open("test-result.txt", "a") as file:
        waktu_uji = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{waktu_uji} - Test {testName} - Status: {status}\n")

# ---------------------------------------- Login ----------------------------------------
try:
    driver.get(url)
    
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    username_input.send_keys(username)
    time.sleep(1)
    password_input.send_keys(password)
    time.sleep(1)
    login_button.click()
    time.sleep(3) 

except Exception as e:
    print(f"Error during login: {e}")
    driver.quit()
    exit()
finally:
    generate_log("Login", "Success" if driver.current_url != url else "Error")

# ---------------------------------------- Order ----------------------------------------
try:
    menu_button = driver.find_element(By.ID, "menu-btn")
    product_list = driver.find_element(By.CSS_SELECTOR, "a[href='/Product/ProductList?category=All']")

    menu_button.click()
    time.sleep(1)
    product_list.click()
    time.sleep(2)

    cards = driver.find_elements(By.CLASS_NAME, "clickable-card")
    first_two_cards = cards[:2]

    for i, card in enumerate(first_two_cards):
        card.click()
        time.sleep(2)

        variant_options = driver.find_elements(By.CLASS_NAME, "variant-option-tag")
        add_cart_btn = driver.find_element(By.ID, "add-cart")
        select_option_number = random.randint(0, len(variant_options) -1)

        variant_options[select_option_number].click()
        time.sleep(1)
        
        add_cart_btn.click()
        time.sleep(2)

    pay_button = driver.find_element(By.ID, "btn-pay")
    pay_button.click()
    time.sleep(3)

    va_option = driver.find_element(By.CLASS_NAME, "collapsible-payment--multiple__body")
    va_option.click()
    time.sleep(2)

    va_bca = driver.find_element(By.CSS_SELECTOR, "a[href='#/bank-transfer/bca-va']")
    va_bca.click()
    time.sleep(2)


except Exception as e:
    print(f"Error during order: {e}")
    driver.quit()
    exit()

