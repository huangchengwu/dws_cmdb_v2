import requests
import zipfile
from celery import Celery

import subprocess

def download_package(path,name,command):
    url = "http://cmdb.keli.vip/DeployCen/Download/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = ("admin", "XEFCJ9DeR7tZIMJy64")
    data = {"path": path,"name":name}
    response = requests.post(url, headers=headers, auth=auth, json=data)
    with open(name, "wb") as f:
        f.write(response.content)
    output = subprocess.check_output(command, shell=True)
    print("===shell",output.decode())


download_package("/var/lib/jenkins/workspace/1700118129-task_run测试","1700118129-task_run测试.tar.gz","ls -l")