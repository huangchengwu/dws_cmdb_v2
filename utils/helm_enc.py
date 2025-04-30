# -*- coding: UTF-8 -*-

import glob
import json

import requests

import tarfile
import os


class Helm:
    def __init__(self, directory="templates/helm/"):
        self.directory = directory

    def newHelm(self, App):
        directory = "templates/helm_package/%s" % (App)
        _charts = directory + "/charts"
        if not os.path.exists(_charts):
            os.mkdir(_charts)

            
        if not os.path.exists(directory):
            os.mkdir(directory)

        chart = os.path.join(directory, "Chart.yaml")
        with open(chart, "w") as file:
            file.write(App.chart)
        values = os.path.join(directory, "values.yaml")
        with open(values, "w") as file:
            file.write(App.values)
        _directory = directory + "/templates"


        for t in App.templates.all():
            if not os.path.exists(_directory):
                os.mkdir(_directory)

            values = os.path.join(_directory, str(t))
            with open(values, "w") as file:
                file.write(str(t.templates))

    def build_helm(self, name, directory, output_file):
        # # 创建 tar.gz 归档文件对象
        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(directory, arcname=name)

    def push_helm(self, filepath):
        url = "https://nexus-01.keli.vip/admin/service/rest/v1/components?repository=helm-repo"
        print("上传",filepath)
        username = "admin"
        password = "admin"

        with open(filepath, "rb") as file:
            files = {"file": file}
            response = requests.post(url, files=files, auth=(username, password))

        if response.status_code == 201:
            print("Upload successful.")
        else:
            print("Upload failed:", response.text,response.status_code)



    def up_helm_dir(self):
        data = []
        # 获取目录列表
        subdirectories = [
            name
            for name in os.listdir(self.directory)
            if os.path.isdir(os.path.join(self.directory, name))
        ]
        for subdir in subdirectories:
            subdir_path = os.path.join(self.directory, subdir)
            if os.path.basename(subdir_path) == ".git":
                continue

            # # 读取 values.yaml 文件内容
            values_file = os.path.join(subdir_path, "values.yaml")
            if os.path.isfile(values_file):
                with open(values_file, "r") as f:
                    values_yaml_content = f.read()
            Chart_file = os.path.join(subdir_path, "Chart.yaml")

            if os.path.isfile(Chart_file):
                with open(Chart_file, "r") as f:
                    Chart_yaml_content = f.read()
            info = {}
            templates = {}
            templates_dir = os.path.join(subdir_path, "templates")
            if os.path.isdir(templates_dir):
                template_files = glob.glob(os.path.join(templates_dir, "*.yaml"))
                for template_file in template_files:
                    with open(template_file, "r") as f:
                        template_content = f.read()
                    templates[os.path.basename(template_file)] = template_content

            info[os.path.basename(subdir_path)] = {
                "Chart.yaml": Chart_yaml_content,
                "values.yaml": values_yaml_content,
                "templates": templates,
            }
            data.append(info)
        return data
