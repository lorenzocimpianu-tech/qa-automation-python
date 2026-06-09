class LoginPage:
    """Gestisce tutti gli elementi e le azioni della pagina di login."""

    URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("input#user-name")
        self.password_input = page.locator("input#password")
        self.login_button = page.locator("input#login-button")
        self.error_message = page.locator("[data-test='error']")

    def navigate(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        return self.error_message.text_content()

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()
