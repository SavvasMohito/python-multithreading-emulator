from prometheus_client.parser import text_string_to_metric_families
import requests
from urllib.request import urlretrieve
from json import loads 

# Download SSL Certificate
urlretrieve("http://172.24.1.14/download", "cert.pem")

# metrics = requests.get("https://172.24.1.14/prometheus/metrics",verify="cert.pem").text

# for family in text_string_to_metric_families(metrics):
#   for sample in family.samples:
#     #if "hydra" in 
#     print("Name: {0} Labels: {1} Value: {2}".format(*sample))

metrics = requests.get("https://172.24.1.14/prometheus/api/v1/label/__name__/values",verify="cert.pem").text
    
metricsDict=loads(metrics)
for metricName in metricsDict['data']:
  if "hydra" in metricName:
    print(metricName)
    hydra_metric = requests.get("https://172.24.1.14/prometheus/api/v1/query?query={}".format(metricName),verify="cert.pem").text
    print(hydra_metric)