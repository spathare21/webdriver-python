import logging
import sys
import unittest
import os
import pytest

from Flow import BasicFlow
from I18n import I18nAuditor
from TestConfig import TestRunConfig
from TestHarness import WebDriverModule


class TestCase(unittest.TestCase):
    """
      Testcase base. The location for adding augments.
    """
    def setup_method(self, method):
        self.init_logging()
        logging.info("Starting %s:%s" % (type(self).__name__, method.__name__))
        # self.i18n_up()

    def teardown_method(self, method):
        logging.info("Finished test " + method.__name__)
        # self.i18n_down()
        BasicFlow.BasicFlow().goto_logout()
        WebDriverModule.WebDriverModule().reload_driver()

    def init_logging(self):
        log_levels = ["DEBUG", "INFO", "WARN"]
        log_location = TestRunConfig.TestRunConfig().get("log_location")
        log_level_str = str(TestRunConfig.TestRunConfig().get("log_level")).upper()
        if log_level_str not in log_levels:
            print("Invalid log level specified '%s', must be %s" % (log_level_str, log_levels))
            raise Exception("Invalid log level specified")
        elif log_level_str == "DEBUG":
            log_level = logging.DEBUG
        elif log_level_str == "WARN":
            log_level = logging.WARN
        else:
            log_level = logging.INFO
        logging.basicConfig(filename=log_location, filemode='w+', level=log_level)
        logging.StreamHandler(sys.stdout)

    @pytest.yield_fixture(scope="session", autouse=True)
    def driver_fixture(self):
        # Shut down the driver when ALL tests are finished
        logging.info("Fixtures set")
        yield
        logging.info("Shutting down WebDriver")
        driverref = WebDriverModule.WebDriverModule().get_driver()
        driverref.close()
        driverref.quit()

    # Augments
    def i18n_up(self):
        # Initiate I18nAuditor
        locale = TestRunConfig.TestRunConfig().get('i18n_locale')
        logging.debug("Locale is %s", locale)
        if locale != 'en_US':
            BasicFlow.BasicFlow().change_language(locale)
        I18nAuditor.I18nAuditor().ready_state(True)

    def i18n_down(self):
        # Disable the I18nAuditor
        logging.debug('Winding down I18nAuditor')
        I18nAuditor.I18nAuditor().ready_state(False)
