import logging

from selenium.webdriver.common.by import By

from I18n import I18nObjects
from Page import SignInPage
from Page.AbstractPage import AbstractPage
from TestConfig import TestRunConfig


class HomePage(AbstractPage):
    """
      Example HomePage. This homepage contains a dropdown menu hiding a login button.
      Clicking the login button sends the user to the Sign In Page.
      When logged in, it shows the user's username.
    """

    DROPDOWN = (By.CLASS_NAME, 'dropdown-toggle')

    def click_login(self):
        logging.info("Click login button")
        self.click_element(self.DROPDOWN)
        self.click_element(self.get_login_button())
        return SignInPage.SignInPage()

    def logged_in_as(self):
        logging.info("Query logged in user")
        return self.get_text(self.DROPDOWN)

    def get_login_button(self):
        locale = TestRunConfig.TestRunConfig().i18n_locale
        link_text = I18nObjects.I18nObjects().translation_for(self.i18n_name, 'Login', locale)
        return (By.LINK_TEXT, link_text)
