import pytest
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    options=Options()
    options.add_argument("--incognito")
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

def test_random_product_selection(driver):
    driver.find_element(By.ID,"user-name").send_keys("standard_user")
    driver.find_element(By.ID,"password").send_keys("secret_sauce")
    driver.find_element(By.ID,"login-button").click()

    time.sleep(2)

    products = driver.find_elements(By.CLASS_NAME,"inventory_item")

    assert len(products)==6, f"Expected 6 products ,but found {len(products)}"

    selected_products = random.sample(products,4)

    for i,product in enumerate(selected_products, start =1):
        name = product.find_element(By.CLASS_NAME,"inventory_item_name").text
        price = product.find_element(By.CLASS_NAME,"inventory_item_price").text
        print(f"product{i}: {name} - {price}")






