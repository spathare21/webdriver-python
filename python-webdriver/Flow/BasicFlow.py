import logging

from Flow.AbstractFlow import AbstractFlow
from Page.HomePage import HomePage
from TestHarness import WebDriverModule


class BasicFlow(AbstractFlow):

    driver = None

    def __init__(self):
        self.driver = WebDriverModule.WebDriverModule().get_driver()

    def goto_home(self):
        logging.info("Go to homepage %s" % self.HOMEPAGE)
        self.driver.get(self.get_host_url())
        return HomePage()

    def goto_logout(self):
        logging.info("Go to logout directly")
        logouturl = self.get_host_url()+"/logout"
        self.driver.get(logouturl)