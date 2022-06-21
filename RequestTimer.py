import time

import RefreshForm
import ReqQuery


def timer():
    time.sleep(0.5)
    time_last_request = time.time()
    time_update_catalog = time.time()
    while True:
        if time.time() - time_last_request > 10:
            if time.time() - time_update_catalog > 3600:
                ReqQuery.get_catalog()
                ReqQuery.update_status()
                RefreshForm.update_info_form()
                RefreshForm.refresh_form()
                time_update_catalog = time.time()
                time_last_request = time.time()
            else:
                ReqQuery.update_status()
                RefreshForm.refresh_form()
                time_last_request = time.time()
        time.sleep(15)

