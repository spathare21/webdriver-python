import logging

from Flow.AbstractFlow import AbstractFlow
from Page.HomePage import HomePage
from selenium.webdriver.common.by import By


class BasicFlow(AbstractFlow):
    """
    Contains the basic workflow actions, such as go to home
    """
    LANGUAGE_SELECT = (By.ID, 'localeBox')

    def goto_home(self):
        logging.info("Go to homepage %s" % self.HOMEPAGE)
        self.driver.get(self.get_host_url())
        return HomePage()

    def goto_logout(self):
        logging.info("Go to logout directly")
        logout_url = self.get_host_url() + "/logout"
        self.driver.get(logout_url)

    def change_language(self, language):
        logging.info('Changing language to %s', language)
        homepage = self.goto_home()
        homepage.select_option(self.LANGUAGE_SELECT, language)
