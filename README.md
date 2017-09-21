# WebDriver Template

## Introduction
This project aims to provide a WebDriver template for Java, Python and Perl, using some quality engineering and development collaboration learnings.

## Features
### Page Knowledge
Each page is detailed as its own entity, so that this information is not lost in test code.
### Flows
Highly repeated steps, such as login, can be shifted to a workflow for shorter test code.
### Logging
An important part of testing is knowing where things are when they break. This system provides a step by step logging method.
### Screenshots
Further to the above, a series of screenshots is a great tool for debugging broken tests.
### Timing
Element waits are built into every action, preventing misses on slow element appearances.
### Chains
Chains can provide a nice, readable test case. For example,<br>
`home_page = BasicFlow.BasicFlow().goto_home()\`<br>
`    .click_login()\`<br>
`    .enter_username('admin')\`<br>
`    .enter_password('password')\`<br>
`    .press_login()`<br>
`self.assertEquals(homepage.logged_in_as(), "admin")`

## Usage
This section details the usage for each of the template flavours.

### Java
... Coming soon

### Python
#### Requirements

* Python 3
* Pytest
* Python Selenium
* polib, difflib and html2text for I18nAuditor
* PIL for annotated screenshots

#### Environment
The following can be set as desired:<br>
`CHROMEDRIVER=/path/to/chromedriver` : Path to the chromedriver executable<br>
`WEBDRIVERHOME="http://the.target.site/"` : The target site under test<br>
`WEBDRIVERLOGLOC="/tmp/logging/webdriver.log` : Logfile location<br>
`WEBDRIVERLOGLEVEL=INFO` : (Optional) Lowest log level, default INFO (of DEBUG, INFO, WARN)<br>
`SCREENSHOTDIR=/tmp/somewhere` : (Optional) Screenshot directory<br>

#### Run
cd Test
pytest-3

#### Augmentations
#### I18n Auditor
This module is designed to record and compare pages between languages.<br>
This process is, currently, very slow. It attempts read, match and reverse match<br>
languages using (at best) .po files. Or at worst, a dictionary.<br>
Use, for example:<br>
`I18NMODE=record I18NLOCALE=en_US pytest-3`<br>
`I18NMODE=compare I18NLOCALE=es_ES pytest-3`<br>


### Perl
... Coming soon
