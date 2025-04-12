import pytest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

def login(driver):
    driver.find_element(By.ID,"user-name").send_keys("standard_user")
    driver.find_element(By.ID,"password").send_keys("secret_sauce")
    driver.find_element(By.ID,"login-button").click()

def test_random_add_to_cart(driver):
    login(driver)

    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"inventory_item")))

    add_to_cart_buttons = driver.find_elements(By.XPATH,"//button[contains(text(),'Add to cart')]")
    assert len(add_to_cart_buttons) >= 6, "Less than 6 products found in inventory"

    selected_buttons = random.sample(add_to_cart_buttons,4)

    for btn in selected_buttons:
        btn.click()

    cart_count = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"shopping_cart_badge"))).text

    assert cart_count == '4', f"Expected 4 items in cart,but found{cart_count}"






    
