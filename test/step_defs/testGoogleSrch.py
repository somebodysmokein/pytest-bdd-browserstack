import pytest
from selenium import webdriver
import sys
import os, json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pytest_bdd import scenario, given, when, then, parsers
#import test.step_defs.conftest

#from environment import start_local, stop_local

#config_file_path = "config/single.json"



@scenario('../features/googlesrch.feature', 'can find search results for BrowserStack')
def test_googlesrch():
    pass

@scenario('../features/googlesrch.feature', 'can find search results for Selenium')
def test_googlesrchforSelenium():
    pass


@given(parsers.parse('I visit url "{google}"'))
def navigate_search_url(browser, google):
    browser.get(google)
    sleep(5)


@when(parsers.parse('I search for "{text}"'))
def go_to_article(browser, text):
    if not "Google" in browser.title:
        raise Exception("Are you not on google? How come!")
    elem = browser.find_element_by_name("q")
    elem.send_keys(text)
    elem.submit()
    browser.implicitly_wait(10)


@then(parsers.parse('title changes to "{title}"'))
def title_change(browser, title):
    print(browser.title)
    assert title == browser.title




