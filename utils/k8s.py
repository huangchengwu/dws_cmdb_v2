# -*- coding: UTF-8 -*-
import kubernetes
from kubernetes.watch import Watch
from kubernetes.client import CoreV1Api
from kubernetes.client.rest import ApiException
from kubernetes.client import CustomObjectsApi


class CrdApiInfo(CustomObjectsApi):
    def list_namespaced_pod_with_http_info(self, namespace, url=None, **kwargs):
        path_params = {"namespace": namespace}
        query_params = [("labelSelector", "app=php"), ("watch", True)]
        return self.api_client.call_api(
            url,
            "GET",
            path_params,
            query_params,
            _return_http_data_only=True,
            _preload_content=False,
        )


kube_config = "~/.kube/config"


def load_config(DEBUG):
    if DEBUG == True:
        kubernetes.config.kube_config.load_kube_config(config_file=kube_config)

    else:
        kubernetes.config.load_incluster_config()


def WatchDo(Cumsum):
    load_config(True)
    w = Watch()
    c = CrdApiInfo()

    for event in w.stream(
        c.list_namespaced_pod_with_http_info,
        namespace="cloud72",
        url="/api/v1/namespaces/{namespace}/pods",
    ):
        event_type = event["type"]
        pod_object = event["object"]

        pod_name = pod_object["metadata"]["name"]
        print("Pod name:", pod_name)


if __name__ == "__main__":
    WatchDo(True)
