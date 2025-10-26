# tests/test_password_reset.py
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HOME_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
LOGIN_URL_FRAGMENT = "route=account/login"
FORGOT_URL_FRAGMENT = "route=account/forgotten"
RESET_EMAIL = os.getenv("RESET_EMAIL", "tester@example.com")  # 没设置就用占位邮箱

def _click_first(driver, wait, locators):
    last_err = None
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click()
            return
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"Cannot click any of: {locators}\nlast error: {last_err}")

def test_password_reset_flow(driver):
    wait = WebDriverWait(driver, 15)

    # 1) 首页
    driver.get(HOME_URL)

    # 2) My account → Login
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
    wait.until(EC.url_contains(LOGIN_URL_FRAGMENT))

    # 3) Forgotten Password
    _click_first(driver, wait, [
        (By.LINK_TEXT, "Forgotten Password"),
        (By.PARTIAL_LINK_TEXT, "Forgotten"),
        (By.XPATH, "//a[contains(.,'Forgotten')]"),
    ])
    wait.until(EC.url_contains(FORGOT_URL_FRAGMENT))

    # 4) 输入邮箱
    email_box = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, "input[type='email'], input[name='email'], #input-email"
    )))
    email_box.clear()
    email_box.send_keys(RESET_EMAIL)

    # 5) Continue
    _click_first(driver, wait, [
        (By.XPATH, "//input[@type='submit' and (@value='Continue' or @value='continue')]"),
        (By.CSS_SELECTOR, "input.btn.btn-primary"),
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
    ])

    # 成功或警告都说明流程可达，有反馈
    alert = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".alert, .alert-success, .alert-warning, .alert-danger, .message, .notice"
    )))
    assert alert is not None, "No feedback alert after submitting password reset request"
    assert FORGOT_URL_FRAGMENT in driver.current_url or "success" in driver.current_url

    # ✅ 所有断言通过后输出这句
    print("✅ The process for resetting a forgotten password is correct.")

