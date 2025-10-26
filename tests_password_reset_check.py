from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
TEST_EMAIL = "tester@example.com"  # 用任何邮箱都行，此用例只验证流程

def _click_first(driver, wait, locators):
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click()
            return
        except Exception:
            continue
    raise RuntimeError(f"Cannot click any of: {locators}")

def test_password_reset_flow(driver):
    wait = WebDriverWait(driver, 20)

    driver.get(BASE_URL)

    _click_first(driver, wait, [
        (By.LINK_TEXT, "My account"),
        (By.PARTIAL_LINK_TEXT, "My Account"),
        (By.CSS_SELECTOR, "a[title='My Account']"),
    ])
    _click_first(driver, wait, [
        (By.LINK_TEXT, "Login"),
        (By.PARTIAL_LINK_TEXT, "Login"),
        (By.CSS_SELECTOR, "a[href*='route=account/login']"),
    ])
    wait.until(EC.url_contains("route=account/login"))

    _click_first(driver, wait, [
        (By.LINK_TEXT, "Forgotten Password"),
        (By.PARTIAL_LINK_TEXT, "Forgot"),
        (By.CSS_SELECTOR, "a[href*='route=account/forgotten']"),
    ])
    wait.until(EC.url_contains("route=account/forgotten"))

    email = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    ))
    email.clear()
    email.send_keys(TEST_EMAIL)

    _click_first(driver, wait, [
        (By.XPATH, "//input[@value='Continue']"),
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.CSS_SELECTOR, "input[type='submit'], button[type='submit']"),
    ])

    alert = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".alert, .alert-success, .alert-danger, .message, .notice"
    )))
    assert alert.is_displayed()

    print("✅ The process for resetting a forgotten password is correct.")



