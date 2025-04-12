import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def setup():
    options = Options()
    options.add_argument("--incognito")  # Open browser in incognito mode
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()


def test_logout_button_functionality(setup):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    time.sleep(1)
    driver.find_element(By.ID, "react-burger-menu-btn").click()

    time.sleep(1)
    logout_button = driver.find_element(By.ID, "logout_sidebar_link")

    assert logout_button.is_displayed(), "Logout button is not visible"
    logout_button.click()

    time.sleep(1)
    assert "https://www.saucedemo.com/" in driver.current_url, "Logout failed or did not redirect to login page"
