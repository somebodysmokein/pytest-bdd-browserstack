import os
from browserstack.local import Local


# Start the tunnel if the browserstack.local is set to true
def start_local():
    """Code to start browserstack local before start of test."""
    global bs_local
    bs_local = Local()
    """Use Local identifier to create parallel tunnels for parallel tests"""
    bs_local_args = {"key": os.environ.get('BROWSERSTACK_ACCESS_KEY'), "forcelocal": "true",
                     "localIdentifier": os.environ.get('BROWSERSTACK_USERNAME') + "_" + os.environ.get('TASK_ID')}
    bs_local.start(**bs_local_args)


# Stop the tunnel if it is still active
def stop_local():
    """Code to stop browserstack local after end of test."""
    global bs_local
    if bs_local is not None:
        bs_local.stop()
