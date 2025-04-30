from celery import shared_task
import requests
import json
import time
from utils.jenkins_server import Jenkins_server
from jinja2 import Template
import io
import zipfile
from ConfCen.views import get_env_info
from ConfCen.models import *
from DeployCen.models import *
from django.forms.models import model_to_dict
from django.core import serializers
import os
from django.conf import settings  # noqa
import yaml
from ProjManage.models import *

jenkins_xml = """<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@1326.ve643e00e9220">
  <actions>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition@2.2144.v077a_d1928a_40"/>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@2.2144.v077a_d1928a_40">
      <jobProperties/>
      <triggers/>
      <parameters/>
      <options/>
    </org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
  </actions>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@3793.v65dec41c3a_c3">
    <script>  {{ pipeline }}
</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
"""
jenkins_parameters = """
    parameters {
    stashedFile 'stashedFile'
    string(name: 'Action', defaultValue: 'deploy', description: '动作')

    }

"""

jenkins_stashedFile = """
                script {
                   if (BUILD_ID == '1') {
                        error("upconfig===")
                    } else {
                        echo "exec task  ${BUILD_ID}"
                    }
                    try {
                        unstash 'stashedFile'
                        sh '''
                             mv stashedFile stashedFile.zip
                             unzip stashedFile.zip
                        '''
                    } catch (Exception e) {
                        echo "Failed to unstash: ${e.getMessage()}"
                        // Add appropriate exception handling here
                    }
                }
                
"""

Debug_temp = """
import yaml
from jinja2 import Template
from colorama import init, Fore, Back, Style
import sys
arguments = sys.argv

init()

# # 读取 YAML 文件
with open('env_info.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)
env_info=yaml_data
temp_filename=arguments[1]

with open(temp_filename, 'r') as file:
    temp = file.read()


 

tp = Template(temp)

content = tp.render(env_info)
print(Fore.BLUE+"=========================模版文件 %s===============" % temp_filename)
 
print(Fore.RED + '''\n=========================渲染前=========================\n''',temp, Fore.GREEN + '''\n=========================渲染后=========================\n''',content)
"""
jenkins_end = """
post {
        success {
            sh "test -f success.sh && success.sh 'success' ${JOB_NAME}  ${BUILD_ID}   ${JENKINS_HOME} ${WORKSPACE}   ${JOB_URL} ${BUILD_DISPLAY_NAME} || echo ''"
        }
        failure {
            sh "test -f failure.sh && failure.sh 'failure' ${JOB_NAME}  ${BUILD_ID}   ${JENKINS_HOME} ${WORKSPACE}   ${JOB_URL} ${BUILD_DISPLAY_NAME} || echo ''"

        }
}
"""


def jenkins_end_tools(success, failure):
    ## success success.sh  成功
    ## success failure.sh  失败

    jenkins_end = """
    post {
            success {
                sh "%s ${JOB_NAME}  ${BUILD_ID}   ${JENKINS_HOME} ${WORKSPACE}   ${JOB_URL} ${BUILD_DISPLAY_NAME} || echo ''"
            }
            failure {
                sh "%s ${JOB_NAME}  ${BUILD_ID}   ${JENKINS_HOME} ${WORKSPACE}   ${JOB_URL} ${BUILD_DISPLAY_NAME} || echo ''"

            }
    }
    """ % (
        success,
        failure,
    )
    return jenkins_end


def http_get_tools(url, headers):
    try:
        h = json.loads(headers)
        # headers = {
        #     'accept': 'application/json',
        #     'X-CSRFToken': 'jzsTgL1qdwE5jZz4Q99vBQcbDeIvJaPOgGceQD8jN96dKeic8KK7s5uwHobJXpg9'
        # }
        response = requests.get(url, headers=h)

        data = response.json()
        data["msg"] = "成功执行"
        return data
    except:
        print("错误解析")
        return {"msg": "错误解析"}


def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()  # 创建一个副本，确保不改变原始字典

    for key, value in dict2.items():
        merged_dict[key] = value  # 使用dict2的值替换dict1中的对应键的值

    return merged_dict


@shared_task(soft_time_limit=300, track_started=True)
def Task_rollback(Id):
    task_deploy_obj = TaskDeploy.objects.get(Id=Id)
    server = Jenkins_server(
        settings.JENKINS_URL,
        username=settings.JENKINS_USER,
        password=settings.JENKINS_PASSWORD,
        timeout=None,
    )

    job_name = "%s-%s" % (
        task_deploy_obj.version,
        task_deploy_obj.taskdeploy_env,
    )
    print("task_rollback", Id, job_name)

    server.build_job_files(job_name, parameters={"files": ""})


# 封装执行
@shared_task(soft_time_limit=300, track_started=True)
def TaskEnc_exec(Id, user, action,version):

    obj = Projdep.objects.get(Id=Id)

    print("执行任务用户请求", Id, user, action, obj.name)


    obj.cid = version
 

    matching_custom_env = Custom_Env.objects.filter(name=obj.name + "项目部署配置")
    #     # 判断是否存在满足条件的数据
    if matching_custom_env.exists():
        matching_custom_env.update(config=obj.ConfigContent)
    else:
        Custom_Env(name=obj.name + "项目部署配置", config=obj.ConfigContent).save()
    ct = Custom_Env.objects.filter(name=obj.name + "项目部署配置")
    Id = obj.TaskEnc_select_Custom_Env.TaskEnctaskcreate.Id
    tc = TaskCreate.objects.filter(Id=Id)
    t = Task_type.objects.filter(Id=tc[0].task_type.Id)
    TaskDeploy(taskdeploy_env=tc[0], task_type=t[0], User=user, version=version).save()
    taskDeploy_obj = TaskDeploy.objects.get(version=version)
    print("taskDeploy_obj.Id",taskDeploy_obj.Id)
    taskDeploy_obj.select_Custom_Env = ct[0]
    taskDeploy_obj.save()
    obj.log_id = taskDeploy_obj.Id
    obj.task_name = tc[0].name
    obj.save()
    build_jenkins_action.delay(taskDeploy_obj.Id, user,action)
    print("执行自定义任务")
    # build_jenkins_.delay(1, "huangchengwu")
    # print("开始执行任务", files)
    # server.build_job_files(job_name, parameters={"files": files, "Action": action})


@shared_task(soft_time_limit=300, track_started=True)
def Task_disable(Id):
    task_deploy_obj = TaskDeploy.objects.get(Id=Id)
    server = Jenkins_server(
        settings.JENKINS_URL,
        username=settings.JENKINS_USER,
        password=settings.JENKINS_PASSWORD,
        timeout=None,
    )
    try:
        job_name = "%s-%s" % (
            task_deploy_obj.version,
            task_deploy_obj.taskdeploy_env,
        )
        print("task_disable", Id, job_name)

        server.delete_job(job_name)
    except:
        print("task异常无需关心")
    task_deploy_obj.delete()


def tools_env(key, version):
    if key == "php":
        return """
    environment {
        PATH = "$PATH:/usr/local/%s-%s"
    }

""" % (
            key,
            version,
        )

    return """tools {
        %s "%s-%s"
    }
""" % (
        key,
        key,
        version,
    )

@shared_task(soft_time_limit=300, track_started=True)
def build_jenkins_action(Id, user,action):
    print("执行任务", Id, user)
    server = Jenkins_server(
        settings.JENKINS_URL,
        username=settings.JENKINS_USER,
        password=settings.JENKINS_PASSWORD,
        timeout=None,
    )

    task_deploy_obj = TaskDeploy.objects.get(Id=Id)

    task_create_obj = TaskCreate.objects.get(Id=task_deploy_obj.taskdeploy_env.Id)

    env_info = get_env_info()
    # 将 uploads/pipeline/test.zip 添加到 ZIP 中

    buffer = io.BytesIO()

    zip_file = zipfile.ZipFile(buffer, "w")
    upload_file = "%s" % task_create_obj.pipeline.pacakge
    if upload_file != "":
        print("上传包", upload_file)
        _upload_file = upload_file.split("/")[-1]
        env_info["upload_file"] = _upload_file
        with open("uploads/%s" % upload_file, "rb") as f:
            zip_file.writestr(_upload_file, f.read())
    env_info["jenkins_parameters"] = jenkins_parameters
    env_info["jenkins_stashedFile"] = jenkins_stashedFile
    env_info["jenkins_end"] = jenkins_end
    env_info["form_k8s_Env"] = str(task_create_obj.k8s_Env)
    env_info["user"] = user
    env_info["form_HostGroup"] = str(task_create_obj.HostGroup)
    env_info["form_pipeline"] = str(task_create_obj.pipeline)
    env_info["templateGroup"] = str(task_create_obj.templateGroup)
    env_info["updated_at"] = "%s" % task_deploy_obj.updated_at
    env_info["created_at"] = "%s" % task_deploy_obj.created_at
    env_info["version"] = "%s" % task_deploy_obj.version
    env_info["task_name"] = "%s" % task_deploy_obj.taskdeploy_env
    env_info["task_type"] = "%s" % task_deploy_obj.task_type
    env_info["Id"] = "%s" % task_deploy_obj.Id

    env_info["form_task_type"] = task_deploy_obj.task_type.templates
    work_dir = "/var/jenkins_home/workspace/%s-%s" % (
        task_deploy_obj.version,
        task_deploy_obj.taskdeploy_env,
    )

    env_info["work_dir"] = work_dir
    print("开始预选自定义变量", task_deploy_obj.select_Custom_Env)
    try:
        custom_Env_data = yaml.safe_load(task_deploy_obj.select_Custom_Env.config)

        env_info = merge_dicts(env_info, custom_Env_data)

    except:
        print("为选自定义变量 跳过处理 或者配置问题请检查")
    print(env_info)
    shell_script_export = ""
    shell_script = ""

    for key, value in env_info.items():
        shell_script_export += f"export {key}='{value}'\n"
    for key, value in env_info.items():
        shell_script += f"{key}='{value}'\n"

    esv = json.dumps(env_info, indent=4)
    env_info["env_info"] = esv
    ya = yaml.dump(env_info)
    try:
        template_group = TemplatesGroup.objects.get(Id=task_create_obj.templateGroup.Id)
        ds = list(template_group.group.all().values())
    except:
        print("未找到模版组忽略")
        ds = []

    for _ds in ds:
        tp = Template(_ds["templates"])
        env_info[_ds["name"]] = tp.render(
            env_info, jenkins_end_tools=jenkins_end_tools, http_get_tools=http_get_tools
        )

        content = tp.render(
            env_info, jenkins_end_tools=jenkins_end_tools, http_get_tools=http_get_tools
        )
        zip_file.writestr(_ds["name"], content)
    zip_file.writestr("env_info.yaml", ya)
    zip_file.writestr("env_info.json", esv)

    zip_file.writestr("shell_script_export", shell_script_export)
    zip_file.writestr("shell_script", shell_script)

    zip_file.writestr("Debug_temp.py", Debug_temp)

    ##调试脚本
    temp = Template(task_create_obj.pipeline.templates)
    pipeline_result = temp.render(
        env_info, jenkins_end_tools=jenkins_end_tools, http_get_tools=http_get_tools
    )
    print("====pipeline_result", pipeline_result)
    zip_file.close()
    filename = "%s-%s.zip" % (task_deploy_obj.version, task_deploy_obj.taskdeploy_env)
    file_path = "uploads/package/" + filename

    with open(file_path, "wb") as file:
        file.write(buffer.getvalue())

    j_xml = Template(jenkins_xml)
    _j_xml = j_xml.render(
        {"pipeline": pipeline_result},
        jenkins_end_tools=jenkins_end_tools,
        http_get_tools=http_get_tools,
    )
    job_name = "%s-%s" % (task_deploy_obj.version, task_deploy_obj.taskdeploy_env)

    if server.job_exists(job_name):
        print("更新job")
        server.reconfig_job(job_name, config_xml=_j_xml)
        server.build_job(job_name)

    else:
        print("创建job")
        server.create_job(job_name, config_xml=_j_xml)
        server.build_job(job_name)
        i = 0

        while True:
            get_build_info = server.get_build_info(job_name, 1)
            result = get_build_info["result"]

            print(result)
            if result == "FAILURE":
                break
            elif result == "SUCCESS":
                break
            time.sleep(1)
            i += 1

    files = {
        "stashedFile": (
            filename,
            open(file_path, "rb"),
        )
    }
 
    print("开始执行任务", files)
    server.build_job_files(job_name, parameters={"files": files, "Action": action})
    Id = server.get_job_info(job_name).get("lastBuild")["number"]
    print("任务类型", task_deploy_obj.task_type.types)


@shared_task(soft_time_limit=300, track_started=True)
def build_jenkins_(Id, user):
    print("执行任务", Id, user)
    server = Jenkins_server(
        settings.JENKINS_URL,
        username=settings.JENKINS_USER,
        password=settings.JENKINS_PASSWORD,
        timeout=None,
    )

    task_deploy_obj = TaskDeploy.objects.get(Id=Id)

    task_create_obj = TaskCreate.objects.get(Id=task_deploy_obj.taskdeploy_env.Id)

    env_info = get_env_info()
    # 将 uploads/pipeline/test.zip 添加到 ZIP 中

    buffer = io.BytesIO()

    zip_file = zipfile.ZipFile(buffer, "w")
    upload_file = "%s" % task_create_obj.pipeline.pacakge
    if upload_file != "":
        print("上传包", upload_file)
        _upload_file = upload_file.split("/")[-1]
        env_info["upload_file"] = _upload_file
        with open("uploads/%s" % upload_file, "rb") as f:
            zip_file.writestr(_upload_file, f.read())
    env_info["jenkins_parameters"] = jenkins_parameters
    env_info["jenkins_stashedFile"] = jenkins_stashedFile
    env_info["jenkins_end"] = jenkins_end
    env_info["form_k8s_Env"] = str(task_create_obj.k8s_Env)
    env_info["user"] = user
    env_info["form_HostGroup"] = str(task_create_obj.HostGroup)
    env_info["form_pipeline"] = str(task_create_obj.pipeline)
    env_info["templateGroup"] = str(task_create_obj.templateGroup)
    env_info["updated_at"] = "%s" % task_deploy_obj.updated_at
    env_info["created_at"] = "%s" % task_deploy_obj.created_at
    env_info["version"] = "%s" % task_deploy_obj.version
    env_info["task_name"] = "%s" % task_deploy_obj.taskdeploy_env
    env_info["task_type"] = "%s" % task_deploy_obj.task_type
    env_info["Id"] = "%s" % task_deploy_obj.Id

    env_info["form_task_type"] = task_deploy_obj.task_type.templates
    work_dir = "/var/jenkins_home/workspace/%s-%s" % (
        task_deploy_obj.version,
        task_deploy_obj.taskdeploy_env,
    )

    env_info["work_dir"] = work_dir
    print("开始预选自定义变量", task_deploy_obj.select_Custom_Env)
    try:
        custom_Env_data = yaml.safe_load(task_deploy_obj.select_Custom_Env.config)

        env_info = merge_dicts(env_info, custom_Env_data)

    except:
        print("为选自定义变量 跳过处理 或者配置问题请检查")
    print(env_info)
    shell_script_export = ""
    shell_script = ""

    for key, value in env_info.items():
        shell_script_export += f"export {key}='{value}'\n"
    for key, value in env_info.items():
        shell_script += f"{key}='{value}'\n"

    esv = json.dumps(env_info, indent=4)
    env_info["env_info"] = esv
    ya = yaml.dump(env_info)
    try:
        template_group = TemplatesGroup.objects.get(Id=task_create_obj.templateGroup.Id)
        ds = list(template_group.group.all().values())
    except:
        print("未找到模版组忽略")
        ds = []

    for _ds in ds:
        tp = Template(_ds["templates"])
        env_info[_ds["name"]] = tp.render(
            env_info, jenkins_end_tools=jenkins_end_tools, http_get_tools=http_get_tools
        )

        content = tp.render(
            env_info, jenkins_end_tools=jenkins_end_tools, http_get_tools=http_get_tools
        )
        zip_file.writestr(_ds["name"], content)
    zip_file.writestr("env_info.yaml", ya)
    zip_file.writestr("env_info.json", esv)

    zip_file.writestr("shell_script_export", shell_script_export)
    zip_file.writestr("shell_script", shell_script)

    zip_file.writestr("Debug_temp.py", Debug_temp)

    ##调试脚本
    temp = Template(task_create_obj.pipeline.templates)
    pipeline_result = temp.render(
        env_info, jenkins_end_tools=jenkins_end_tools, http_get_tools=http_get_tools
    )
    print("====pipeline_result", pipeline_result)
    zip_file.close()
    filename = "%s-%s.zip" % (task_deploy_obj.version, task_deploy_obj.taskdeploy_env)
    file_path = "uploads/package/" + filename

    with open(file_path, "wb") as file:
        file.write(buffer.getvalue())

    j_xml = Template(jenkins_xml)
    _j_xml = j_xml.render(
        {"pipeline": pipeline_result},
        jenkins_end_tools=jenkins_end_tools,
        http_get_tools=http_get_tools,
    )
    job_name = "%s-%s" % (task_deploy_obj.version, task_deploy_obj.taskdeploy_env)

    if server.job_exists(job_name):
        print("更新job")
        server.reconfig_job(job_name, config_xml=_j_xml)
        server.build_job(job_name)

    else:
        print("创建job")
        server.create_job(job_name, config_xml=_j_xml)
        server.build_job(job_name)
        i = 0

        while True:
            get_build_info = server.get_build_info(job_name, 1)
            result = get_build_info["result"]

            print(result)
            if result == "FAILURE":
                break
            elif result == "SUCCESS":
                break
            time.sleep(1)
            i += 1

    files = {
        "stashedFile": (
            filename,
            open(file_path, "rb"),
        )
    }

    print("开始执行任务", files)
    server.build_job_files(job_name, parameters={"files": files})
    Id = server.get_job_info(job_name).get("lastBuild")["number"]
    print("任务类型", task_deploy_obj.task_type.types)
