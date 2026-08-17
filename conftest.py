import pytest
import os
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
AUTH_FILE = "playwright/.auth/state.json"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True
    }

@pytest.fixture(scope="session")
def logged_in_storage(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()
    try:
        login_page = LoginPage(page)
        page.goto("https://www.amazon.in/")
        login_page.login(USERNAME, PASSWORD)
        os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
        context.storage_state(path=AUTH_FILE)
    finally:
        context.close()
        browser.close()
    return AUTH_FILE

@pytest.fixture(scope="function")
def auth_page(browser, logged_in_storage):
    context = browser.new_context(storage_state=logged_in_storage)
    # context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    # trace_path = f"traces/trace.zip"
    # os.makedirs("traces", exist_ok=True)
    # context.tracing.stop(path=trace_path)
    page.close()
    context.close()