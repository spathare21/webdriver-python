from TestHarness import WebDriverModule
import os


class AbstractFlow:

    HOMEPAGE = os.environ["WEBDRIVERHOME"]

    # def __init__(self):
    #     self.driver = WebDriverModule.WebDriverModule().get_driver()

    def get_host_url(self):
        return self.HOMEPAGE
