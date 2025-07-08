import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import time

# ---------------------------------------- Initialize ---------------------------------------- 
url = "http://localhost:5101/auth/login"
url_order = "http://localhost:5101/order/createorder"

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

    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    title = driver.find_element(By.XPATH, "//div[@class='collapsible-payment--multiple__title']")
    title.click()
    time.sleep(2)

    va_bca = driver.find_element(By.CSS_SELECTOR, "a[href='#/bank-transfer/bca-va']")
    va_bca.click()
    time.sleep(5)

    copy_va = driver.find_element(By.XPATH, "//div[@class='float-right clickable copy']")
    copy_va.click()
    time.sleep(2)

    driver.execute_script("window.open('https://simulator.sandbox.midtrans.com/bca/va/index', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    merchant_input = driver.find_element(By.ID, "inputMerchantId")
    merchant_input.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)

    inquire_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    inquire_button.click()
    time.sleep(2)

    pay_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    pay_button.click()
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.frame(iframe)
    time.sleep(2)

    check_status_btn = driver.find_element(By.XPATH, "//button[@class='btn full primary  btn-theme']")
    check_status_btn.click()
    time.sleep(20)

except Exception as e:
    print(f"Error during order: {e}")
    driver.quit()
    exit()
finally:
    generate_log("Order", "Success" if driver.current_url == url_order else "Error")