import pytest
import os
import csv
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

def pytest_addoption(parser):
    parser.addoption(
        "--export-csv",
        action="store",
        default=None,
        metavar="FILE_PATH",
        help="Export all discovered test case names and file paths to the specified CSV file."
    )


def pytest_collection_modifyitems(config, items):
    csv_filename = config.getoption("--export-csv")
    if not csv_filename:
        return

    print(f"\n[CSV Export] Discovering tests and writing to: {csv_filename}...")
    directory = os.path.dirname(csv_filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Test Case Name", "File Path", "Line Number"])

        for item in items:
            test_name = item.name
            file_path = str(item.path)
            line_no = item.location[1] + 1
            writer.writerow([test_name, file_path, line_no])

    print(f"[CSV Export] Successfully exported {len(items)} test cases.")
    pytest.exit("Test cases successfully exported to CSV. Skipping execution.", returncode=0)
