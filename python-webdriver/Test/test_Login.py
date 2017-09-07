from Flow.BasicFlow import BasicFlow
from TestHarness.TestCase import TestCase


class test_Login(TestCase):
    """
      Example test. This test is for a successful login, that uses the chained steps for
      ease of reading.
    """
    def test_login(self):
        homepage = BasicFlow().goto_home()\
            .click_login()\
            .enter_username("admin")\
            .enter_password("redhat123")\
            .click_log_in()
        self.assertEquals(homepage.logged_in_as(), "admin@internal")

    def test_login_failure(self):
        signinpage = BasicFlow().goto_home() \
            .click_login() \
            .enter_username("user") \
            .enter_password("password") \
            .click_log_in_expectfail()
        self.assertTrue(signinpage.is_login_failure())
