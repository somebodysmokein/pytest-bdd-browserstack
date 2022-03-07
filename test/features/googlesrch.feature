Feature: Google\'s Search Functionality
    Scenario: can find search results for BrowserStack
        Given I visit url "http://www.google.com/ncr"
        When I search for "BrowserStack"
        Then title changes to "BrowserStack - Google Search"

    Scenario: can find search results for Selenium
        Given I visit url "http://www.google.com/ncr"
        When I search for "Selenium"
        Then title changes to "Selenium - Google Search"