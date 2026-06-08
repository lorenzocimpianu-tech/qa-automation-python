import pytest
import requests
from playwright.sync_api import sync_playwright

# --- Costanti separate dalla logica di test ---
SAUCEDEMO_URL = "https://www.saucedemo.com/"
SAUCEDEMO_USER = "standard_user"
SAUCEDEMO_PASS = "secret_sauce"

@pytest.fixture
def create_test_user():
    """
    Simula la creazione di un utente via API.
    Nota: jsonplaceholder è un mock — non valida i campi,
    ma ci permette di testare il pattern fixture + assert sul codice HTTP.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": "qa_tester_python",       # jsonplaceholder usa 'title', non 'username'
        "body": "tester@example.com",
        "userId": 1
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 201, (
        f"Creazione utente fallita: {response.status_code} - {response.text}"
    )

    data = response.json()
    # Restituiamo un dizionario con chiavi coerenti per il test
    return {
        "id": data["id"],
        "username": SAUCEDEMO_USER,  # In un sistema reale, verrebbe dall'API
        "password": SAUCEDEMO_PASS,
    }


def test_user_login_flow(create_test_user):
    """
    Testa il flusso di login su SauceDemo usando le credenziali
    'ricevute' dalla fase API (qui simulate con utenti predefiniti).
    """
    user_data = create_test_user
    username = user_data["username"]
    password = user_data["password"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # True per CI, False per debug locale
        page = browser.new_page()

        try:
            page.goto(SAUCEDEMO_URL)

            page.fill("input#user-name", username)
            page.fill("input#password", password)
            page.click("input#login-button")

            # Verifica URL post-login
            assert "inventory.html" in page.url, (
                f"Redirect inatteso dopo login: {page.url}"
            )

            # Verifica titolo catalogo
            titolo = page.locator("span.title").text_content()
            assert titolo == "Products", f"Titolo inatteso: '{titolo}'"

        finally:
            browser.close()  # Garantito anche in caso di errore