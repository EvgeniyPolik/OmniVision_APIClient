import time
from threading import Thread

import RefreshForm
import ReqQuery


def timer():
    time.sleep(0.5)
    time_last_request = time.time()
    while True:
        if time.time() - time_last_request > 15:
            ReqQuery.update_status()
            RefreshForm.refresh_form()
            if time.time() - time_last_request > 3600:
                ReqQuery.get_catalog()
            time_last_request = time.time()