import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
URL = "https://www.saucedemo.com/"

# Fixture with Incognito Mode
@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--incognito")  # Enable incognito
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(URL)
    yield driver
    driver.quit()

# Login helper
def login(browser, username, password):
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

# Test case
def test_cart_button_visible(browser):
    login(browser, USERNAME, PASSWORD)
    wait = WebDriverWait(browser, 10)
    cart_btn = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_link")))
    assert cart_btn.is_displayed(), "Cart button is not visible"
    print("Cart button is visible.")
