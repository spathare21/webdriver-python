import logging

from selenium.webdriver.common.by import By

from Page import HomePage
from Page.AbstractPage import AbstractPage


class SignInPage(AbstractPage):
    """
      Example Sign In Page. This page contains a username field, password field and log in button.
      Clicking the login button returns the user to the homepage, if successful.
    """

    # LOCATOR
    USERNAMEFIELD = (By.ID, "username")
    PASSWORDFIELD = (By.ID, "password")
    LOGINBUTTON = (By.CLASS_NAME, "btn")
    LOGINFAILURE = (By.CLASS_NAME, "row")

    # PAGE TEXT
    LOGINFAILUREMESSAGE = "Unable to log in. Verify your login information or contact the system administrator."

    def enter_username(self, username):
        logging.info("Enter username " + username)
        self.enter_text(self.USERNAMEFIELD, username)
        return SignInPage()

    def enter_password(self, password):
        logging.info("Enter password " + password)
        self.enter_text(self.PASSWORDFIELD, password)
        return SignInPage()

    def click_log_in(self):
        logging.info("Click sign in button")
        self.click_element(self.LOGINBUTTON)
        return HomePage.HomePage()

    def click_log_in_expectfail(self):
        logging.info("Click sign in button")
        self.click_element(self.LOGINBUTTON)
        return SignInPage()

    def is_login_failure(self):
        logging.info("Query failure message shown")
        return self.element_contains_text(self.LOGINFAILURE, self.LOGINFAILUREMESSAGE)