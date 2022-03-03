from paver.easy import *
from paver.setuputils import setup
import threading, os, platform

setup(
    name = "pytest-bdd-browserstack",
    version = "1.0.0",
    author = "BrowserStack",
    author_email = "support@browserstack.com",
    description = ("Pytest BDD Integration with BrowserStack"),
    license = "MIT",
    keywords = "example pytest bdd browserstack",
    url = "https://github.com/ashwingonsalves/pytest-bdd-browserstack",
    packages=['test']
)

def run_pytest_bdd(config, feature, task_id=0):
    if platform.system() == 'Windows':
        sh('SET CONFIG_FILE=config/%s.json & SET TASK_ID=%s & pytest test/step_defs/%s.py -v -s' % (config, task_id, feature))
    else:
        sh('export CONFIG_FILE=config/%s.json && export TASK_ID=%s && pytest test/step_defs/%s.py -v -s' % (config, task_id, feature))

@task
@consume_nargs(2)
def run(args):
    """Run single, local and parallel test using different config."""
    if args[0] in ('single', 'local'):
        run_pytest_bdd(args[0], args[1])
    else:
        jobs = []
        for i in range(4):
            p = threading.Thread(target=run_pytest_bdd,args=(args[0], args[1],i))
            jobs.append(p)
            p.start()

        for th in jobs:
         th.join()

@task
def test():
    """Run all tests"""
    sh("paver run single")
    sh("paver run local")
    sh("paver run parallel")