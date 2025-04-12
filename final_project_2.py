import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_guvi_user():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get("https://www.saucedemo.com/")  # Replace with your actual URL if different

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Wait for successful login indicator (e.g., inventory page)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

        # Basic check - page has inventory list
        assert "inventory" in driver.current_url or "inventory_list" in driver.page_source

    finally:
        driver.quit()
