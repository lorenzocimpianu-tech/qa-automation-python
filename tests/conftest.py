import pytest
import os

# Cartella dove vengono salvati gli screenshot
SCREENSHOT_DIR = "reports/screenshots"


def pytest_configure(config):
    """Crea la cartella screenshot all'avvio della sessione."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pytest: cattura uno screenshot automaticamente
    quando un test UI fallisce nella fase di esecuzione (call).
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Recupera la fixture 'page' dal test (se esiste)
        page = item.funcargs.get("page")
        if page is not None:
            test_name = item.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")
            screenshot_path = f"{SCREENSHOT_DIR}/{test_name}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n📸 Screenshot salvato: {screenshot_path}")
            except Exception as e:
                print(f"\n⚠️ Screenshot fallito: {e}")
