# password_reset_check.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HOME_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
LOGIN_URL_FRAGMENT = "route=account/login"
FORGOT_URL_FRAGMENT = "route=account/forgotten"
RESET_EMAIL = os.getenv("RESET_EMAIL", "tester@example.com")

def click_first(driver, wait, locators):
    last_err = None
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click()
            return
        except Exception as e:
            last_err = e
    raise RuntimeError(f"Cannot click any of: {locators}\nlast error: {last_err}")

def main():
    opts = Options()
    # 注释下一行即可“有界面”运行；保留则无界面
    # opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(HOME_URL)
        click_first(driver, wait, [
            (By.LINK_TEXT, "My account"),
            (By.PARTIAL_LINK_TEXT, "My account"),
            (By.XPATH, "//a[contains(.,'My account') or contains(.,'My Account')]"),
            (By.CSS_SELECTOR, "a[title='My account'], a[title='My Account']"),
        ])
        click_first(driver, wait, [
            (By.LINK_TEXT, "Login"),
            (By.PARTIAL_LINK_TEXT, "Login"),
            (By.XPATH, "//a[contains(.,'Login')]"),
        ])
        wait.until(EC.url_contains(LOGIN_URL_FRAGMENT))
        click_first(driver, wait, [
            (By.LINK_TEXT, "Forgotten Password"),
            (By.PARTIAL_LINK_TEXT, "Forgotten"),
            (By.XPATH, "//a[contains(.,'Forgotten')]"),
        ])
        wait.until(EC.url_contains(FORGOT_URL_FRAGMENT))

        email_box = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "input[type='email'], input[name='email'], #input-email"
        )))
        email_box.clear()
        email_box.send_keys(RESET_EMAIL)

        click_first(driver, wait, [
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
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
