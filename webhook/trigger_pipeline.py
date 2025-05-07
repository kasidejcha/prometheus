from fastapi import FastAPI, Request
import uvicorn
import os
from datetime import datetime
import json

app = FastAPI()


# define the endpoint for handling incoming alerts
@app.post('/alert')
async def alert(request: Request):
    # get the JSON payload from the request
    data = await request.json()
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(dt)
    # extract the alert name and status
    for alert in data['alerts']:
        alert_name = alert['labels']['alertname']
        alert_status = alert['status']
        print('Alert:', alert)
        
        # check if the alert status is firing
        if alert_status == 'firing':
            print("trigger airflow CT dag")
            alert_source = alert['labels']['source']
            alert_severity = alert['labels']['severity']
            print(f'alert_name: {alert_name} | alert_source: {alert_source} | alert_severity: {alert_severity} | alert_status: {alert_status}')
            
            # execute the Bash script
            with open(os.path.join('data', 'current_alert.json'), "w") as outfile:
                json.dump(alert, outfile, indent=2)
            os.system('/home/kasidej/Documents/prometheus/webhook/trigger_airflow_dag.sh')

                
            break
    return {"status": "success"}


if __name__ == '__main__':
    uvicorn.run("trigger_pipeline:app", host="192.168.242.139", port=5000, reload=True)
