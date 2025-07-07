from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time
from selenium.webdriver.support.ui import Select

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

    # Navigate to Inventory
    menu_button = driver.find_element(By.CSS_SELECTOR, ".rounded-circle.circle-wrapper")
    menu_button.click()
    time.sleep(1)

    inventory_button = driver.find_element(By.CSS_SELECTOR, ".bi.bi-box-seam.me-3")
    inventory_button.click()
    time.sleep(1)

    add_inventory_button = driver.find_element(By.CSS_SELECTOR, ".bi.bi-patch-plus")
    add_inventory_button.click()
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

# ---------------------------------------- Fill Inventory Form ----------------------------------------

try:
    name = "Tepung Terigu"
    category = "Setengah Jadi"
    stock = "100"
    unit = "kilogram"
    price = "61000"
    lower_limit = "0"
    note = "Disimpan di tempat kering"

    driver.find_element(By.ID, "name").send_keys(name)
    time.sleep(1)

    Select(driver.find_element(By.ID, "category")).select_by_visible_text(category)
    time.sleep(1)

    driver.find_element(By.ID, "stock").send_keys(stock)
    time.sleep(1)

    Select(driver.find_element(By.ID, "unit")).select_by_visible_text(unit)
    time.sleep(1)

    driver.find_element(By.ID, "price").send_keys(price)
    time.sleep(1)

    driver.find_element(By.ID, "lower-limit").send_keys(lower_limit)
    time.sleep(1)

    driver.find_element(By.ID, "note").send_keys(note)
    time.sleep(3)

    # Klik tombol submit
    driver.find_element(By.XPATH, "//button[contains(text(), 'Add Item')]").click()
    time.sleep(2)

    generate_log("AddInventory", "Success")

except Exception as e:
    print(f"Error during inventory form submission: {e}")
    generate_log("AddInventory", "Error")
    driver.quit()
    exit()
