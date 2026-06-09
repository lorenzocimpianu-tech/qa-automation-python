import pytest
import requests

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# --- Costanti separate dalla logica di test ---
SAUCEDEMO_USER = "standard_user"
SAUCEDEMO_PASS = "secret_sauce"

# --- Fixture ---

@pytest.fixture(scope="session")
def api_user():
    """
    Simula la creazione di un utente via API.
    scope="session" → viene eseguita una volta sola per tutti i test.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": "qa_tester_python",
        "body": "tester@example.com",
        "userId": 1,
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201, (
        f"Creazione utente fallita: {response.status_code} - {response.text}"
    )
    data = response.json()
    return {
        "id": data["id"],
        "username": SAUCEDEMO_USER,
        "password": SAUCEDEMO_PASS,
    }


# --- Test: happy path ---

def test_login_success(page, api_user):
    """
    Verifica il login corretto e la visualizzazione del catalogo prodotti.
    'page' è la fixture nativa di pytest-playwright — il conftest
    può intercettarla automaticamente per gli screenshot on failure.
    """
    login = LoginPage(page)
    login.navigate()
    login.login(api_user["username"], api_user["password"])

    inventory = InventoryPage(page)

    assert inventory.is_loaded(), (
        f"Redirect inatteso dopo login: {page.url}"
    )
    assert inventory.get_title() == "Products", (
        f"Titolo inatteso: '{inventory.get_title()}'"
    )


def test_add_product_to_cart(page, api_user):
    """Verifica che aggiungere un prodotto aggiorni il contatore del carrello."""
    login = LoginPage(page)
    login.navigate()
    login.login(api_user["username"], api_user["password"])

    inventory = InventoryPage(page)
    assert inventory.get_cart_count() == 0

    inventory.add_product_to_cart("sauce-labs-backpack")
    assert inventory.get_cart_count() == 1


# --- Test: scenari negativi (parametrizzati) ---

INVALID_CREDENTIALS = [
    ("locked_out_user", SAUCEDEMO_PASS,  "Sorry, this user has been locked out"),
    ("standard_user",   "wrong_password", "Username and password do not match"),
    ("",                "",               "Username is required"),
    ("standard_user",   "",               "Password is required"),
]


@pytest.mark.parametrize("username,password,expected_error", INVALID_CREDENTIALS)
def test_login_failure(page, username, password, expected_error):
    """
    Verifica che il login fallisca con messaggio d'errore corretto
    per diversi scenari di credenziali non valide.
    """
    login = LoginPage(page)
    login.navigate()
    login.login(username, password)

    assert login.is_error_visible(), "Messaggio di errore non visualizzato"
    assert expected_error in login.get_error_message(), (
        f"Errore atteso: '{expected_error}'\n"
        f"Errore ottenuto: '{login.get_error_message()}'"
    )
