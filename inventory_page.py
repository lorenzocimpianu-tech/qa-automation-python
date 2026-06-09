class InventoryPage:
    """Gestisce tutti gli elementi e le azioni della pagina catalogo prodotti."""

    EXPECTED_URL_FRAGMENT = "inventory.html"
    EXPECTED_TITLE = "Products"

    def __init__(self, page):
        self.page = page
        self.title = page.locator("span.title")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

def is_loaded(self, timeout: int = 10_000) -> bool:
    try:
        self.page.wait_for_url(f"**/{self.EXPECTED_URL_FRAGMENT}", timeout=timeout)
        return True
    except Exception:
        return False

    def get_title(self) -> str:
        return self.title.text_content()

    def add_product_to_cart(self, product_name: str):
        """Aggiunge un prodotto al carrello cercandolo per nome."""
        button_locator = self.page.locator(
            f"[data-test='add-to-cart-{product_name.lower().replace(' ', '-')}']"
        )
        button_locator.click()

    def get_cart_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.text_content())

    def go_to_cart(self):
        self.cart_icon.click()
