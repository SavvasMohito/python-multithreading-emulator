import csv
import os


def save_script_metrics(metrics):
    if not (os.path.exists('metrics')):
        os.mkdir('metrics')
        os.mkdir('metrics/devices')
    path = "metrics/scripts.csv"
    input_type = "a" if (os.path.exists(path)) else "w"    

    with open(path, input_type) as csvfile:
            fieldnames = ['SCRIPT_NAME', 'SCRIPT_TIME']
            writer = csv.DictWriter(csvfile,delimiter=';', fieldnames=fieldnames)
            if input_type == 'w' :
                writer.writeheader()
            for metric in metrics:
                writer.writerow(metric)


def save_device_metric(metric,dev_name):
    path = "metrics/devices/{}.csv".format(dev_name)
    input_type = "a" if (os.path.exists(path)) else "w"    

    with open(path, input_type) as csvfile:
            fieldnames = ['EVENT','DURATION','RESPONSE_CODE','TIMESTAMP']
            writer = csv.DictWriter(csvfile,delimiter=';', fieldnames=fieldnames)
            if input_type == 'w' :
                writer.writeheader()
            writer.writerow(metric)

