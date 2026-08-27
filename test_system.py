import time

from actions.system import (
    open_task_manager,
    open_settings
)

print("Testing Task Manager...")
open_task_manager()

time.sleep(2)

print("Testing Windows Settings...")
open_settings()