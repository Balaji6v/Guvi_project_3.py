import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture
def setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


def login(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


def test_checkout_flow_full(setup):
    driver = setup
    login(driver)

    # Add product to cart
    product_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn_inventory")))
    assert product_buttons, "No products found to add to cart."
    driver.execute_script("arguments[0].click();", product_buttons[0])
    time.sleep(1)

    # Check cart count
    cart_badge = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert cart_badge.text == "1", "Cart count not correct."

    # Go to cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    # Screenshot before checkout
    driver.save_screenshot("before_checkout_click.png")

    # Proceed to checkout
    checkout_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_btn.click()

    # Fill checkout info
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # Wait for overview page and take screenshot
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "summary_info")))
    driver.save_screenshot("checkout_overview.png")

    # (Optional) Verify product still in overview
    checkout_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(checkout_items) == 1, "Unexpected number of products in checkout overview."

    # Finish order
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "finish"))).click()

    # Verify confirmation
    complete_header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
    assert "THANK YOU FOR YOUR ORDER" in complete_header.text.upper(), "Order completion message not found."

    print("Test case 8 passed: Full checkout flow successful.")
