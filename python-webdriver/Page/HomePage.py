import logging

from selenium.webdriver.common.by import By

from Page import SignInPage
from Page.AbstractPage import AbstractPage


class HomePage(AbstractPage):
    """
      Example HomePage. This homepage contains a dropdown menu hiding a login button.
      Clicking the login button sends the user to the Sign In Page.
      When logged in, it shows the user's username.
    """

    DROPDOWN = (By.CLASS_NAME, 'dropdown-toggle')
    LOGINBUTTON = (By.LINK_TEXT, 'Login')

    def click_login(self):
        logging.info("Click login button")
        self.click_element(self.DROPDOWN)
        self.click_element(self.LOGINBUTTON)
        return SignInPage.SignInPage()

    def logged_in_as(self):
        logging.info("Query logged in user")
        return self.get_text(self.DROPDOWN)
