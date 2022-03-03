import json
import os
import sys
import pytest
from selenium import webdriver
from test.step_defs.environment import start_local, stop_local

config_file_path = os.environ['CONFIG_FILE'] if 'CONFIG_FILE' in os.environ else 'config/single.json'
TASK_ID = int(os.environ['TASK_ID']) if 'TASK_ID' in os.environ else 0

print("Path to the config file = %s" % (config_file_path))
with open(config_file_path) as config_file:
    CONFIG = json.load(config_file)

# Edit these to match your credentials
USERNAME = os.environ.get('BROWSERSTACK_USERNAME') or sys.argv[1]
BROWSERSTACK_ACCESS_KEY = os.environ.get('BROWSERSTACK_ACCESS_KEY') or sys.argv[2]

if not (USERNAME and BROWSERSTACK_ACCESS_KEY):
    raise Exception("Please provide your BrowserStack username and access key")


# Instantiate the Webdriver module with BrowserStack Capabilities

@pytest.fixture()
def browser():
    url = "https://%s:%s@hub.browserstack.com/wd/hub" % (
        USERNAME, BROWSERSTACK_ACCESS_KEY
    )
    desired_capabilities = CONFIG['environments'][TASK_ID]
    for key in CONFIG["capabilities"]:
        if key not in desired_capabilities:
            desired_capabilities[key] = CONFIG["capabilities"][key]

    if os.getenv("BROWSERSTACK_LOCAL") is not None:
        desired_capabilities["browserstack.local"] = os.getenv("BROWSERSTACK_LOCAL")
    if os.getenv("BROWSERSTACK_BUILD_NAME") is not None:
        desired_capabilities["build"] = os.getenv("BROWSERSTACK_BUILD_NAME")

    if "browserstack.local" in desired_capabilities and desired_capabilities["browserstack.local"]:
        desired_capabilities["browserstack.localIdentifier"] = USERNAME + "_" + str(TASK_ID)
        start_local()
    b = webdriver.Remote(command_executor=url, desired_capabilities=desired_capabilities)

    yield b
    b.quit()
    if "browserstack.local" in desired_capabilities and desired_capabilities["browserstack.local"]:
        stop_local()


# Enter any code that has to run before scenario is called
def pytest_bdd_before_scenario(request, feature, scenario):
    print("inside pytest_bdd_before_scenario")


# Once the step completes successfully, get the fixture which has the driver object and mark the test as failure
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    print("Step passed: inside pytest_bdd_after_step")
    print(step)
    # updateTestResults(browser, "pass")
    context = request.getfixturevalue('browser')
    context.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {'
                           '"status":"passed", "reason": "All assertions passed"}}')


# If one of the assertion fails, get the fixture which has the driver object and mark the test as failure
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print("Step Failed: inside pytest_bdd_step_error")
    print(step)
    print(exception)
    # updateTestResults(browser, "failed")
    context = request.getfixturevalue('browser')
    context.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "At '
        'least 1 assertion failed"}}')
