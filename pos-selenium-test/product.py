from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time
from selenium.webdriver.support.ui import Select
import os

# ---------------------------------------- Initialize ---------------------------------------- 
url = "http://localhost:5101/auth/login"

# User
username = "admin"
password = "Admin@123"

driver = webdriver.Chrome()

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
    time.sleep(1)

    menu_button = driver.find_element(By.CSS_SELECTOR, ".rounded-circle.circle-wrapper")
    menu_button.click()
    time.sleep(1)

    product_button = driver.find_element(By.CSS_SELECTOR, ".bi.bi-bag-plus.me-3")
    product_button.click()
    time.sleep(1)

except Exception as e:
    print(f"Error during login: {e}")
    driver.quit()
    exit()
finally:
    try:
        generate_log("Login", "Success" if driver.current_url != url else "Error")
    except:
        generate_log("Login", "Error (driver closed)")

# ---------------------------------------- Fill Product Form ----------------------------------------

try:
    name = "Roti Kacang"
    description = "Roti kacang dengan rasa manis dan gurih."
    category = "Makanan"
    product_image = "sate-telur-puyuh.webp"
    stock = "200"
    price = "2000"
    
    time.sleep(1)

    driver.find_element(By.ID, "name").send_keys(name)
    time.sleep(1)

    driver.find_element(By.ID, "description").send_keys(description)
    time.sleep(1)

    Select(driver.find_element(By.ID, "category")).select_by_visible_text(category)
    time.sleep(1)

    # Upload Gambar Produk
    image_path = os.path.abspath(product_image)  # Pastikan file roti.jpg ada di direktori project
    driver.find_element(By.ID, "productImage").send_keys(image_path)
    time.sleep(1)

    is_available_checkbox = driver.find_element(By.ID, "isAvailable")
    if not is_available_checkbox.is_selected():
        is_available_checkbox.click()
    time.sleep(1)

    stock_input = driver.find_element(By.ID, "stock")
    stock_input.clear()
    stock_input.send_keys(stock)
    time.sleep(1)

    price_input = driver.find_element(By.ID, "product-price")
    price_input.clear()
    price_input.send_keys(price)
    time.sleep(3)

    driver.find_element(By.XPATH, "//button[contains(text(), 'Save Product')]").click()
    time.sleep(3)

    generate_log("AddProduct", "Success")

except Exception as e:
    print(f"Error during product form submission: {e}")
    generate_log("AddProduct", "Error")
    driver.quit()
    exit()
