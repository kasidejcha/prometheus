from prometheus_api_client import PrometheusConnect
import pandas as pd
from datetime import datetime
import os

host = 'http://10.15.11.106:9090'
prom = PrometheusConnect(url=host)
result = prom.custom_query('ALERTS')


alertname = []
alertstate = []
serverity = []
source = []
value = []
for i in result:
    print(i)
    alertname.append(i['metric']['alertname'])
    alertstate.append(i['metric']['alertstate'])
    serverity.append(i['metric']['serverity'])
    source.append(i['metric']['source'])
    value.append(i['value'][1])

dt = [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]*len(value)
alert = pd.DataFrame([alertname, alertstate, serverity, source, value, dt]).T
alert.columns = ['alertname', 'alertstate', 'serverity', 'source', 'value', 'datetime']
print(alert)

os.system('/home/kasidej/Documents/prometheus/webhook/trigger_airflow_dag.sh')