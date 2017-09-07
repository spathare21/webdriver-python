import logging
import os
import sys
import unittest

import pytest

from Flow import BasicFlow
from TestHarness import WebDriverModule


class TestCase(unittest.TestCase):
    """
      Testcase base
    """
    def setup_method(self, method):
        self.init_logging()
        logging.info("\n%s:%s" % (type(self).__name__, method.__name__))

    def teardown_method(self, method):
        logging.info("Finished test " + method.__name__)
        BasicFlow.BasicFlow().goto_logout()
        WebDriverModule.WebDriverModule().reload_webdriver()

    def init_logging(self):
        loglevel = logging.INFO
        loglevels = ["DEBUG", "INFO", "WARN"]
        loglevelloc = os.environ.get("WEBDRIVERLOGLOC")
        if "WEBDRIVERLOGLEVEL" in os.environ:
            loglevelstr = os.environ["WEBDRIVERLOGLEVEL"]
            if loglevelstr not in loglevels:
                print("Invalid log level specified '%s', must be %s" % (loglevelstr, loglevels))
            if loglevelstr == "DEBUG":
                loglevel = logging.DEBUG
            elif loglevelstr == "WARN":
                loglevel = logging.WARN
            else:
                loglevel = logging.INFO
        logging.basicConfig(filename=loglevelloc, filemode='w', level=loglevel)
        logging.StreamHandler(sys.stdout)

    @pytest.yield_fixture(scope="session", autouse=True)
    def driver_fixture(self):
        logging.info("Fixtures set")
        yield
        logging.info("Shutting down WebDriver")
        driverref = WebDriverModule.WebDriverModule().get_driver()
        driverref.close()
        driverref.quit()