import subprocess
import ctypes
import time


def lock_pc():
    ctypes.windll.user32.LockWorkStation()


def sleep_pc():
    subprocess.run(
        ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
        check=False
    )


def restart_pc():
    subprocess.run(
        ["shutdown", "/r", "/t", "5"],
        check=False
    )


def shutdown_pc():
    subprocess.run(
        ["shutdown", "/s", "/t", "5"],
        check=False
    )


def cancel_shutdown():
    subprocess.run(
        ["shutdown", "/a"],
        check=False
    )


def open_task_manager():
    subprocess.Popen("taskmgr.exe")


def open_settings():
    subprocess.Popen("start ms-settings:", shell=True)