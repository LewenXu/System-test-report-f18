import os
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras
def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Show real Chrome window")
@pytest.fixture
def driver(request):
    headed = request.config.getoption("--headed") or os.getenv("HEADED") == "1"
    opts = Options()
    if not headed:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    d = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    yield d
    d.quit()
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call" or rep.passed:
        return
    drv = item.funcargs.get("driver")
    if not drv:
        return
    Path("artifacts").mkdir(exist_ok=True)
    img = Path("artifacts") / f"{item.name}.png"
    drv.save_screenshot(str(img))
    rep.extra = getattr(rep, "extra", [])
    rep.extra.append(extras.image(str(img)))
