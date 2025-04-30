#!coding:utf-8
import requests
import json
from jinja2 import Template


class Aargo:
    def __init__(self, user, password, server):
        self.server = server
        self.token = None
        self.user = user
        self.password = password
        self.data = None
        self.headers = None
        self.config = {
            "name": "k8s-khadgar",
            "namespace": "argocd",
            "targetRevision": " 0.3.0",
            "repoURL": "http://172.16.0.226:31413",
            "chart": "java-temp",
            "server": "https://kubernetes.default.svc",
        }
        self.temp = """
                        {
                            "metadata": {
                            "name": "{{ name }}",
                            "namespace": "{{  namespace }}"
                            },
                            "spec": {
                            "source": {
                                "repoURL": "{{ repoURL }}",
                                "targetRevision": "{{ targetRevision }}",
                                "helm": {
                                "valueFiles": [
                                    "values.yaml"
                                ],
                                "values": ""
                                },
                                "chart": "{{ chart }}"
                            },
                            "destination": {
                                "server": "{{ server }}",
                                "namespace": "{{ namespace }}"
                            },
                            "project": "default",
                            "syncPolicy": {
                                "automated": {
                                "selfHeal": true
                                },
                                "syncOptions": [
                                "CreateNamespace=true"
                                ]
                            }
                            }
                        }
                        """
        t = Template(self.temp)
        self.temp = t.render(self.config)
        self.data = json.loads(self.temp)
        url = self.server + "/api/v1/session"
        res = requests.post(
            url,
            '{"username":"%s","password":"%s"}' % (self.user, self.password),
            verify=False,
        )
        data = json.loads(res.text)
        token = data["token"]
        self.headers = {"Authorization": "Bearer %s" % (token)}

    def create(self, values):
        url = self.server + "/api/v1/applications"
        self.data["spec"]["source"]["helm"]["values"] = values
        Params = json.dumps(self.data, indent=4)
        r = requests.post(url, Params, headers=self.headers, verify=False)
        print(url, r.text)

    def delete(self, name):
        url = self.server + "/api/v1/applications/%s" % (name)
        r = requests.delete(url, headers=self.headers, verify=False)
        print(url, r.text)

    def update(self, name, values):
        url = self.server + "/api/v1/applications/%s" % (name)
        self.data["spec"]["source"]["helm"]["values"] = (
            repr(values)
            .replace("\\n", "\n")
            .replace("\\r", "")
            .replace("u", "")
            .replace("'", "")
        )
        Params = json.dumps(self.data, indent=4)
        r = requests.put(url, Params, headers=self.headers, verify=False)
        print(url, r.text)

    def logs(self, name):
        url = self.server + "/api/v1/applications/%s/logs" % (name)
        r = requests.get(url, headers=self.headers, verify=False)
        print(url, r.text)

    def status_watch(self):
        pass


if "__main__" == __name__:
    a = Aargo(
        user="admin", password="2fJIPhwtokpDhgA6", server="https://172.16.0.226:32184"
    )
    # a.create(values=u'name : khadgar\r\nport : 8060\r\ngit : http://git.doumob.club/service/khadgar.git\r\npath: khadgar*.jar\r\nlog : /data/logs/app\r\nconfig : dev\r\nversion: "20220301181504"\r\ndescribe : \u517b\u6210\u6e38\u620f')
    # a.delete("k8s-khadgar")
    # a.logs("k8s-khadgar")
    a.update(
        "k8s-khadgar",
        values='name : khadgar\nport : 1010\ngit : http://git.doumob.club/service/khadgar.git\npath: khadgar*.jar\nlog : /data/logs/app\nconfig : dev\nversion: "20220301181504"\ndescribe : \\u517b\\u6210\\u6e38\\u620f\n',
    )
