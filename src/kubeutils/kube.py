import json
import os

from kubernetes import client, config
from kubernetes.client.rest import ApiException

config.load_kube_config(config_file=os.environ.get('KUBE_CONFIG_PATH'))
v1 = client.CoreV1Api()
conf_path = os.environ.get('CLUSTER_CONFIG')


class Kube:
    def logs(self, namespace, pod, **kwargs):
        try:
            # kwargs['tail_lines'] = 100
            api_response = v1.read_namespaced_pod_log(pod, namespace, **kwargs)
            return api_response
        except ApiException as e:
            print('Found exception in reading the logs')

    def writeLogs(self, ns, pod):
        filelog = open('tmp/%s.txt' % pod, 'w')
        filelog.write(self.logs(ns, pod))
        filelog.close()
        return pod

    def namespaces(self):
        try:
            namespaces_list = v1.list_namespace()
            for item in namespaces_list.items:
                print(item.metadata.name)
        except ApiException as e:
            raise Exception('Found exception in reading the namespaces')

    def pods(self, namespace):
        text = ""
        try:
            namespaces_list = v1.list_namespaced_pod(namespace=namespace)
            for item in namespaces_list.items:
                text = text + f"{item.metadata.name} | status: {item.status.phase} | restarts: {item.status.container_statuses[0].restart_count}" \
                              f" | Creation Time: {item.metadata.creation_timestamp} \n"
        except Exception as e:
            raise Exception('Found exception in reading the namespaces')
        return text

    def setCluster(self, env, cluster):
        try:
            with open(conf_path, "r") as jsonfile:
                data = json.load(jsonfile)
                if env == "QE":
                    config.load_kube_config(config_file=data["BASE_PATH"] + data[env][cluster])
        except Exception as e:
            print('Found exception in setting the cluster conf')

    def getCluster(self, env):
        text = ""
        with open(conf_path, "r") as jsonfile:
            data = json.load(jsonfile)
            if env == "QE":
                for k in data[env]:
                    text = text + k + '\n'
        return text


if __name__ == "__main__":
    kbcl = Kube()
    # (kbcl.pods('metricsgateway'))
    (kbcl.namespaces())
