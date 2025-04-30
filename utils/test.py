import requests
import sys
import json

# files={
#         'large': ('1695901740-硬盘读写测试模版.zip', open('/tmp/1695901740-硬盘读写测试模版.zip', 'rb'))
# }
# url = "http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/10/api/json?depth=0"
auth = ("admin", "118f338a6b38c0bd8776b5da8e683b0e3c")

build_url  = f'http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/build'
response = requests.post(build_url, auth=auth)

print(response.text)
# response = requests.get(url, auth=auth)
# data = json.loads(response.text)
# print(data["result"])

# if data["result"] == None:
#     print("执行中")
# elif data["result"] == "FAILURE":
#     print("执行失败")
# elif data["result"] == "SUCCESS":
#     print("执行成功")

# response = requests.post(url, auth=auth,files=files)
# print(response.raise_for_status)


#       import requests

#         jenkins_url = "http://103.63.139.18:30025"
#         pipeline_job_name = "%s-%s" % (version, template_group.name)
#         auth = ("admin", "118f338a6b38c0bd8776b5da8e683b0e3c")  # Jenkins的用户名和密码

#         # 构建请求的URL和XML配置
#         job_url = f"{jenkins_url}/job/{pipeline_job_name}/config.xml"
#         headers = {"Content-Type": "text/xml; charset=utf-8"}

#         # 检查job是否已存在
#         response = requests.get(job_url, auth=auth)

#         if response.status_code == 200:
#             # 更新现有job的配置

#             update_url = f"{jenkins_url}/job/{pipeline_job_name}/config.xml"
#             print("更新现有job的配置", update_url, response.status_code)

#             response = requests.post(
#                 update_url, auth=auth, headers=headers, data=_j_xml.encode("utf-8")
#             )
#             response.raise_for_status()
#         else:
#             # 创建新的job
#             create_url = f"{jenkins_url}/createItem?name={pipeline_job_name}"

#             response = requests.post(
#                 create_url, auth=auth, headers=headers, data=_j_xml.encode("utf-8")
#             )
#             response.raise_for_status()

#         # server.build_job_url(pipeline_job_name)
#         # reload_url = f'http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/reload'
#         # response = requests.post(reload_url, auth=auth)

#         # # 检查响应状态码
#         # if response.status_code == 200:
#         #     print("重新加载配置成功",response.status_code)
#         # else:
#         #     print("重新加载配置失败")

#         reload_url = f'http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/build'
#         response = requests.post(reload_url, auth=auth)

#         # 检查响应状态码
#         if response.status_code == 200:
#             print("编译成功",response.status_code)
#         else:
#             print("编译成功")

#         files={
#                 'large': ('1695901740-硬盘读写测试模版.zip', open('uploads/package/1695901740-硬盘读写测试模版.zip', 'rb'))
#         }

#         url = 'http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/buildWithParameters'
#         auth = ('admin', '118f338a6b38c0bd8776b5da8e683b0e3c')

#         response = requests.post(url, auth=auth,files=files)
#         print(response.raise_for_status)

#         print("===")


    # jenkins_url = "http://103.63.139.18:30025"

    # pipeline_job_name = "%s-%s" % (version, job_name)

    # auth = ("admin", "118f338a6b38c0bd8776b5da8e683b0e3c")  # Jenkins的用户名和密码

    # job_url = f"{jenkins_url}/job/{pipeline_job_name}/config.xml"
    # headers = {"Content-Type": "text/xml; charset=utf-8"}

    # response = requests.get(job_url, auth=auth)

    # if response.status_code == 200:
    #     # 更新现有job的配置

    #     update_url = f"{jenkins_url}/job/{pipeline_job_name}/config.xml"
    #     print("更新现有job的配置", update_url, response.status_code)

    #     response = requests.post(
    #         update_url, auth=auth, headers=headers, data=_j_xml.encode("utf-8")
    #     )
    #     response.raise_for_status()
    # else:
    #     # 创建新的job
    #     create_url = f"{jenkins_url}/createItem?name={pipeline_job_name}"

    #     response = requests.post(
    #         create_url, auth=auth, headers=headers, data=_j_xml.encode("utf-8")
    #     )
    #     response.raise_for_status()

    # reload_url = f"http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/build"
    # response = requests.post(reload_url, auth=auth)

    # # curl -w %{http_code}  -u admin:118f338a6b38c0bd8776b5da8e683b0e3c   http://103.63.139.18:30025/job/1695901740-硬 盘读写测试模版/lastBuild/consoleText
    # # 检查响应状态码

    # status_url = "http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/lastBuild/api/json"
    # response = requests.get(status_url, auth=auth)
    # data = json.loads(response.text)
    # id = int(data["id"]) + 1

    # time.sleep(10)

    # files = {
    #     "large": (
    #         "1695901740-硬盘读写测试模版.zip",
    #         open("uploads/package/1695901740-硬盘读写测试模版.zip", "rb"),
    #     )
    # }

    # url = "http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/buildWithParameters"
    # auth = ("admin", "118f338a6b38c0bd8776b5da8e683b0e3c")

    # response = requests.post(url, auth=auth, files=files)

    # status_url = (
    #     "http://103.63.139.18:30025/job/1695901740-硬盘读写测试模版/%s/consoleText" % id
    # )
    # print(status_url, "status_url", id)
    # response = requests.get(status_url, auth=auth)

    # print("text", response.text)

    # if data["result"] == None:
    #     print("执行中")
    # elif data["result"] == "FAILURE":
    #     print("执行失败", json.dumps(data, indent=4))

    # elif data["result"] == "SUCCESS":
    #     print("执行成功")
