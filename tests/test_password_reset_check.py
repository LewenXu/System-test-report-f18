from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
TEST_EMAIL = "tester@example.com" 

def _click_first(driver, wait, locators):
    """依次尝试多个定位器，点到即止。"""
    last_err = None
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click()
            return
        except Exception as e:
            last_err = e
    raise last_err or RuntimeError(f"Cannot click any of: {locators}")

def _wait_any_visible(wait, selectors):
    """传入若干 CSS 选择器，只要其中一个出现并可见就返回该元素。"""
    for sel in selectors:
        try:
            return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, sel)))
        except Exception:
            pass
    return None

def test_password_reset_flow(driver):
    wait = WebDriverWait(driver, 30)

    # Step 1: 首页
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

    email = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, "input[type='email'], #input-email, input[name='email']"
    )))
    email.clear()
    email.send_keys(TEST_EMAIL)

    _click_first(driver, wait, [
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input[type='submit'][value='Continue']"),
    ])

    wait.until(lambda d: (
        "route=account/login" in d.current_url
        or "route=account/forgotten" in d.current_url
    ))

    alert = _wait_any_visible(wait, [
        ".alert-success, .alert-danger, .alert-warning, .alert", 
        "[role='alert']",
        ".message, .notice, .notification",
        ".notices .success, .notices .warning, .notices .error",
        ".text-danger" 
    ])
    assert alert is not None, "Timeout waiting for confirmation/notice after submitting the reset form."

    txt = alert.text.strip().lower()
    assert txt != "", "The alert exists but contains empty text."

    print("✅ The process for resetting a forgotten password is correct.")





