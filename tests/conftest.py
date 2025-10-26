# tests/conftest.py
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras

def pytest_addoption(parser):
    # 本地想看浏览器窗口：运行 pytest 时加 --headed
    parser.addoption("--headed", action="store_true", help="Show real Chrome window")

@pytest.fixture
def driver(request):
    headed = request.config.getoption("--headed")
    opts = Options()
    if not headed:                      # 默认无界面；传 --headed 时会显示窗口
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    yield d
    d.quit()

# 失败自动截图（在 pytest-html 的 Links 栏可见）
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call" or rep.passed or "driver" not in item.fixturenames:
        return
    Path("artifacts").mkdir(exist_ok=True)
    png = f"artifacts/{item.name}.png"
    item.funcargs["driver"].save_screenshot(png)
    rep.extra = getattr(rep, "extra", [])
    rep.extra.append(extras.image(png))
