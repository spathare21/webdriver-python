import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestHarness import WebDriverModule


class AbstractPage:
    """
     AbstractPage provides generic user actions, such as clicking and entering text.

    """
    driver = None

    def __init__(self):
        self.driver = WebDriverModule.WebDriverModule().get_driver()
        # TODO wait for images to finish loading

    def element_ready(self, locator):
        logging.debug("Waiting for element ready %s" % str(locator))
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))

    def click_element(self, locator):
        logging.debug("Click element %s" % str(locator))
        element = self.element_ready(locator)
        element.click()

    def enter_text(self, locator, text):
        logging.debug("Enter text element %s" % str(locator))
        element = self.element_ready(locator)
        element.send_keys(text)

    def get_text(self, locator):
        logging.debug("Query text element %s" % str(locator))
        element = self.element_ready(locator)
        return element.text

    def element_contains_text(self, locator, expected):
        # TODO locator for error
        elementtext = self.element_ready(locator).text
        logging.info("Expect %s" % expected)
        logging.info("Found %s" % elementtext)
        logging.info("Is %s in %s" % (expected, elementtext))
        return expected in elementtext
