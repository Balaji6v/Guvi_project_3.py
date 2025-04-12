import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")) )

def test_cart_verification(setup):
    driver = setup
    login(driver)

    #Add the first product to cart
    try:
        add_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_inventory")))
        add_button.click()
        print("Product added to cart")
    except Exception as e:
        driver.save_screenshot("add_product_error.png")
        pytest.fail(f" Failed to add product to cart: {e}")

    # 🧮 Confirm cart badge shows count
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        print(" Cart badge confirmed")
    except:
        driver.save_screenshot("cart_badge_missing.png")
        pytest.fail(" Cart badge did not appear after adding product")

    #  Click cart button
    try:
        cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "shopping_cart_container")))
        cart_button.click()
        print(" Cart button clicked")
    except Exception as e:
        driver.save_screenshot("cart_click_error.png")
        pytest.fail(f"Cart button not clickable: {e}")

    # Verify products in cart
    try:
        product_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))
        print(f"Found {len(product_elements)} product(s) in cart")
    except:
        driver.save_screenshot("cart_empty.png")
        pytest.fail("No products found in cart.")

    # 🔍 Validate product info
    for product in product_elements:
        name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
        price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
        print(f"Product: {name}, Price: {price}")
        assert name.strip() != "", "Product name is empty"
        assert price.strip() != "", "Product price is empty"
