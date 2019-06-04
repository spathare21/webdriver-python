import logging


class TestLog:

    webdriverlog = logging.getLogger('WebDriver')

    def __init__(self):
        TestLog.webdriverlog = logging.getLogger('WebDriver')

    @staticmethod
    def info(msg):
        TestLog.webdriverlog.info(msg)