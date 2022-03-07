from time import sleep
from pytest_bdd import scenario, given, when, then, parsers


# Instantiate a test using test_* method
@scenario('../features/googlesrch.feature', 'can find search results for BrowserStack')
def test_googlesrch():
    pass


# Instantiate a test using test_* method
@scenario('../features/googlesrch.feature', 'can find search results for Selenium')
def test_googlesrchforSelenium():
    pass


@given(parsers.parse('I visit url "{google}"'))
def navigate_search_url(browser, google):
    browser.get(google)
    browser.implicitly_wait(10)
    sleep(5)


@when(parsers.parse('I search for "{text}"'))
def go_to_article(browser, text):
    browser.implicitly_wait(10)
    if not "Google" in browser.title:
        raise Exception("Are you not on google? How come!")
    elem = browser.find_element_by_name("q")
    elem.send_keys(text)
    elem.submit()
    browser.implicitly_wait(10)


@then(parsers.parse('title changes to "{title}"'))
def title_change(browser, title):
    browser.implicitly_wait(10)
    print(browser.title)
    assert title == browser.title
