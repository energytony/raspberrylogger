import os
import shutil
import subprocess
import time
from timeloop import Timeloop
from datetime import timedelta
import redis 
 
 
from datetime import datetime
base_directory = "/home/tonyho/data"
tl = Timeloop()

def mount_usb_drive(device_name='/dev/sda1', mount_point='/mnt/usb'):
    if not os.path.isdir(mount_point):
        os.makedirs(mount_point)
    mount_cmd = 'sudo mount {} {}'.format(device_name, mount_point)
    process = subprocess.Popen(mount_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return True, mount_point
    else:
        print("Error mounting {}: {}".format(device_name, stderr.decode()))
        return False, None

def unmount_usb_drive(mount_point='/mnt/usb'):
    umount_cmd = 'sudo umount {}'.format(mount_point)
    subprocess.Popen(umount_cmd, shell=True)

def list_recently_updated_files(directory, hours=24):
    current_time = time.time()
    cutoff_time = current_time - (hours * 3600)  # Convert hours to seconds
    recently_updated_files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            last_modified_time = os.path.getmtime(filepath)
            if last_modified_time > cutoff_time:
                recently_updated_files.append(filepath)
    return recently_updated_files

def copy_updated_files(files, destination):
    for file in files:
        shutil.copy(file, destination)
        print("Copied {} to {}".format(file, destination))


@tl.job(interval=timedelta(hours=1 ))  # Change to timedelta(hours=6) for every 6 hours
def mainprogram ():
    usb_mounted, usb_mount_point = mount_usb_drive()
    if usb_mounted:
        print("USB drive mounted at {}. Starting to check for updated files.".format(usb_mount_point))
        updated_files = list_recently_updated_files('/home/tonyho/data', 24)  # Check for files updated in the last 24 hours
        if updated_files:
            print("Copying updated files to USB drive.")
            copy_updated_files(updated_files, usb_mount_point)
        else:
            print("No recently updated files to copy.")
        unmount_usb_drive(usb_mount_point)
        print("USB drive unmounted.")
    else:
        print("Failed to mount USB drive.")
        pass 

if __name__ == "__main__":
    print("Save USB Program starting...")
    tl.start(block=True)
