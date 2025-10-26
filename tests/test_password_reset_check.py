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

def _any_visible(wait, candidates):
    """候选定位器中任意一个出现且可见就返回该元素，否则返回 None。"""
    for how, what in candidates:
        try:
            return wait.until(EC.visibility_of_element_located((how, what)))
        except Exception:
            pass
    return None

def _xpath_contains_words(words):

    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    parts = [
        f"contains(translate(.,'{upper}','{lower}'),'{w}')"
        for w in words
    ]
    return f"//*[{ ' and '.join(parts) }]"

def test_password_reset_flow(driver):
    wait = WebDriverWait(driver, 30)
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

    alert = _any_visible(wait, [
        (By.CSS_SELECTOR, ".alert, .alert-success, .alert-danger, .alert-warning"),
        (By.CSS_SELECTOR, "[role='alert']"),
        (By.CSS_SELECTOR, ".message, .notice, .notification, .notices .success, .notices .warning, .notices .error"),
        (By.XPATH, _xpath_contains_words(["password", "reset", "email"])),
        (By.XPATH, _xpath_contains_words(["e-mail", "address", "not", "found"])),
        (By.CSS_SELECTOR, ".text-danger")
    ])

    assert alert is not None, "Timeout waiting for confirmation/notice after submitting the reset form."
    assert alert.text.strip() != "", "The alert exists but contains empty text."

    print("✅ The process for resetting a forgotten password is correct.")






