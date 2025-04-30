import jenkins,json
 
server = jenkins.Jenkins('http://cmdb.keli.vip:8080', username="admin", password="XEFCJ9DeR7tZIMJy64",timeout=None)


# 获取指定Job的Workspace路径
job_name = '1699346317-历史任务删除'
# server.build_job(job_name)
job_info = server.get_job_info(job_name) 
print(job_info)
# print (json.dumps(job_info ,indent=4))


 

# if server.job_exists("1695901740-硬盘读写测试模版") :
#     print("更新job")
#     server.reconfig_job("1695901740-硬盘读写测试模版",config_xml=config_xml)
#     job_name = "1695901740-硬盘读写测试模版"
#     job = server.get_job(job_name)
#     job.invoke()
# else:
#     print("创建job")
#     server.create_job("1695901740-硬盘读写测试模版",config_xml=config_xml)

#     job_name = "1695901740-硬盘读写测试模版"
#     job = server.get_job(job_name)
#     job.invoke()
# server.build_job("1695901740-硬盘读写测试模版")

 