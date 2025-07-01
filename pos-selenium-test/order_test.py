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
    cards = driver.find_elements(By.CLASS_NAME, "card-body")
    first_two_cards = cards[:1]

    for i, card in enumerate(first_two_cards):
        i.clik();

except Exception as e:
    print(f"Error during order: {e}")
    driver.quit()
    exit()

