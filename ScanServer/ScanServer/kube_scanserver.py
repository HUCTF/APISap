import yaml

scanserver_yaml = {'apiVersion': 'apps/v1', 'kind': 'Deployment', 'metadata': {'name': 'scanserver-deployment-{}'}, 'spec': {'selector': {'matchLabels': {'app': 'scanserver-{}'}}, 'replicas': 1, 'template': {'metadata': {'labels': {'app': 'scanserver-{}'}}, 'spec': {'containers': [{'name': 'scanserver-{}', 'image': 'scanserver', 'imagePullPolicy': 'IfNotPresent', 'env': [{'name': 'USERNAME', 'value': 'a{}'}, {'name': 'WEBSITE', 'value': 'a{}'}, {'name': 'RUNWAY', 'value': 'a{}'}, {'name': 'USERCOOKIE1', 'value': 'a{}'}, {'name': 'USERCOOKIE2', 'value': 'a{}'}]}]}}}}

def create_deployment(username, website, runway, usercookie):
    scanserver_yaml['metadata']['name'] = 'scanserver-deployment-{}'.format(username)
    # deployment name
    scanserver_yaml['spec']['selector']['matchLabels']['app'] = 'scanserver-{}'.format(username)
    # app name
    scanserver_yaml['spec']['template']['metadata']['labels']['app'] = 'scanserver-{}'.format(username)
    # labels name
    scanserver_yaml['spec']['template']['spec']['containers'][0]['name'] = 'scanserver-{}'.format(username)
    # container name

    scanserver_yaml['spec']['template']['spec']['containers'][0]['env'][0]['value'] = username
    scanserver_yaml['spec']['template']['spec']['containers'][0]['env'][1]['value'] = website
    scanserver_yaml['spec']['template']['spec']['containers'][0]['env'][2]['value'] = runway
    scanserver_yaml['spec']['template']['spec']['containers'][0]['env'][3]['value'] = usercookie
    scanserver_yaml['spec']['template']['spec']['containers'][0]['env'][4]['value'] = usercookie
    y =  yaml.dump(scanserver_yaml, default_flow_style=False)

    print(y)

create_deployment('tom', 'https://www.baidu.com', 'cookie', '1=1')
