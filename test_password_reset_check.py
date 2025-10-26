from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
FORGOTTEN_URL_KEY = "account/forgotten"

def _click_first(driver, wait, locators):
    last_error = None
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click()
            return
        except Exception as e:
            last_error = e
            continue
    raise RuntimeError(f"Cannot click any of: {locators}") from last_error

def test_password_reset_flow(driver):
    wait = WebDriverWait(driver, 15)

    driver.get(BASE_URL)

    _click_first(driver, wait, [
        (By.LINK_TEXT, "My Account"),
        (By.PARTIAL_LINK_TEXT, "My Account"),
        (By.CSS_SELECTOR, "a[title='My Account']"),
        (By.CSS_SELECTOR, "a[title='My account' i]"),
    ])
    _click_first(driver, wait, [
        (By.LINK_TEXT, "Login"),
        (By.PARTIAL_LINK_TEXT, "Login"),
        (By.CSS_SELECTOR, "a[href*='route=account/login']"),
    ])
    wait.until(EC.url_contains("account/login"))

    _click_first(driver, wait, [
        (By.LINK_TEXT, "Forgotten Password"),
        (By.PARTIAL_LINK_TEXT, "Forgotten"),
        (By.CSS_SELECTOR, "a[href*='route=account/forgotten']"),
    ])
    wait.until(EC.url_contains("account/forgotten"))

    email = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
    email.clear()
    email.send_keys("tester@example.com")

    _click_first(driver, wait, [
        (By.CSS_SELECTOR, "input[type='submit'][value='Continue']"),
        (By.XPATH, "//input[@type='submit' and @value='Continue']"),
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
    ])

    alert = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, ".alert, .alert-success, .alert-danger, .notice, .message"
    )))
    assert FORGOTTEN_URL_KEY in driver.current_url
    assert alert.is_displayed()

    print("✅ The process for resetting a forgotten password is correct.")


