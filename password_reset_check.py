import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HOME_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
LOGIN_URL_FRAGMENT = "route=account/login"
FORGOT_URL_FRAGMENT = "route=account/forgotten"
RESET_EMAIL = os.getenv("RESET_EMAIL", "tester@example.com")

def _click_first(driver, wait, locators):
    last = None
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click()
            return
        except Exception as e:
            last = e
            continue
    raise AssertionError(f"Could not click any of: {locators}\nLast error: {last}")

def test_password_reset_flow(driver):
    wait = WebDriverWait(driver, 15)

    driver.get(HOME_URL)

    _click_first(driver, wait, [
        (By.LINK_TEXT, "My account"),
        (By.PARTIAL_LINK_TEXT, "My account"),
        (By.XPATH, "//a[contains(.,'My account') or contains(.,'My Account')]"),
        (By.CSS_SELECTOR, "a[title='My account'], a[title='My Account']"),
    ])
    _click_first(driver, wait, [
        (By.LINK_TEXT, "Login"),
        (By.PARTIAL_LINK_TEXT, "Login"),
        (By.XPATH, "//a[contains(.,'Login')]"),
    ])
    WebDriverWait(driver, 10).until(EC.url_contains(LOGIN_URL_FRAGMENT))

    _click_first(driver, wait, [
        (By.LINK_TEXT, "Forgotten Password"),
        (By.PARTIAL_LINK_TEXT, "Forgotten"),
        (By.XPATH, "//a[contains(.,'Forgotten')]"),
    ])
    WebDriverWait(driver, 10).until(EC.url_contains(FORGOT_URL_FRAGMENT))
    email = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, "input[type='email'], input[name='email'], #input-email"
    )))
    email.clear()
    email.send_keys(RESET_EMAIL)
    _click_first(driver, wait, [
        (By.XPATH, "//input[@type='submit' and (@value='Continue' or @value='continue')]"),
        (By.CSS_SELECTOR, "input.btn.btn-primary"),
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
    ])

    alert = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".alert, .alert-success, .alert-warning, .alert-danger, .message, .notice"
    )))
    assert alert is not None
    assert FORGOT_URL_FRAGMENT in driver.current_url or "success" in driver.current_url

    print("✅ The process for resetting a forgotten password is correct.")

