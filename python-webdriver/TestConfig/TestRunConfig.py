import os

class TestRunConfig:
    """
    Holds the configuration for the test run
    """

    config_complete = False
    # Defaults - DO NOT USE THESE DIRECTLY! Use get(name)!
    # Path to the chromedriver executable
    driver_path = "chromedriver"
    # Base directory for screenshots
    screenshot_dir = "/tmp/testrun/screenshots/"
    # Base logging level, INFOR, WARN, DEBUG
    log_level = "INFO"
    # Location to store the webdriver log
    log_location = "/tmp/testrun/webdriver.log"
    # I18n Audit mode - off, record, compare
    i18n_audit = "off"
    # Location of i18n audit files
    i18n_audit_dir = "/tmp/testrun/i18n/"
    # Language
    i18n_locale = 'en_US'

    @staticmethod
    def read_config():
        """
        Read the configuration from ENV
        :return: None
        """
        if TestRunConfig.config_complete:
            pass
        # Chrome Driver
        if "CHROMEDRIVER" in os.environ:
            TestRunConfig.driver_path = os.environ.get("CHROMEDRIVER")
        # Screenshot folder
        if "SCREENSHOTDIR" in os.environ:
            TestRunConfig.screenshot_dir = os.environ.get("SCREENSHOTDIR")
        # Logging level
        if "WEBDRIVERLOGLEVEL" in os.environ:
            TestRunConfig.log_level = os.environ.get("WEBDRIVERLOGLEVEL")
        # Logging location (filename)
        if "WEBDRIVERLOGLOC" in os.environ:
            TestRunConfig.log_location = os.environ.get("WEBDRIVERLOGLOC")
        # I18n Auditor mode
        if "I18NMODE" in os.environ:
            TestRunConfig.i18n_audit = os.environ.get("I18NMODE")
        if "I18NLOCALE" in os.environ:
            TestRunConfig.i18n_locale = os.environ.get("I18NLOCALE")
        # Done
        TestRunConfig.config_complete = True

    @staticmethod
    def get(name):
        """
        Returns a config value, ensuring they are set.
        Raises an exception on an invalid name.
        :param name: name of value, e.g driver_path
        :return: value of config name.
        """
        TestRunConfig.read_config()
        if not getattr(TestRunConfig, name):
            raise Exception("Invalid TestRunConfig name requested")
        return getattr(TestRunConfig, name)
