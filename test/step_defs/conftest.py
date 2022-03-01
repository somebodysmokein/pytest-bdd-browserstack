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


@pytest.fixture(scope="session")
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
        start_local()
    b = webdriver.Remote(command_executor=url, desired_capabilities=desired_capabilities)
    b.implicitly_wait(10)
    yield b
    b.quit()
    if "browserstack.local" in desired_capabilities and desired_capabilities["browserstack.local"]:
        stop_local()


def pytest_bdd_before_scenario(request, feature, scenario):
    print("inside pytest_bdd_before_scenario")


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    print("inside pytest_bdd_after_step")
    print('Step passed: {step}')


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print("inside pytest_bdd_step_error")
    print('Step failed: {step} due to exception {exception}')
