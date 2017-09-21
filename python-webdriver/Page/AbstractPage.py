import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from I18n import I18nObjects
from I18n import I18nAuditor
from TestHarness import WebDriverModule


class AbstractPage:
    """
     AbstractPage provides generic user actions, such as clicking and entering text.

    """
    driver = None
    i18n_name = ''

    def __init__(self):
        self.driver = WebDriverModule.WebDriverModule().get_driver()
        # TODO wait for images to finish loading
        self.i18n_name = self.__class__.__name__
        # I18nObjects.I18nObjects().clear_cache()
        # I18nAuditor.I18nAuditor().perform(self.driver, self.i18n_name)

    def element_ready(self, locator):
        logging.info("Waiting for element ready %s" % str(locator))
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
        logging.info("Query element contains %s", expected)
        # TODO locator for error
        element_text = self.element_ready(locator).text
        logging.debug("Expect %s" % expected)
        logging.debug("Found %s" % element_text)
        logging.debug("Is %s in %s" % (expected, element_text))
        return expected in element_text

    def select_option(self, locator, optionname):
        select = Select(self.element_ready(locator))
        if optionname not in select.all_selected_options:
            # Don't select if already selected
            select.select_by_value(optionname)

    def get_i18n_name(self):
        return self.i18n_name
