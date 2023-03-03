from fastapi import FastAPI, Request
from prometheus_client import Counter, make_asgi_app
import subprocess
import uvicorn
import os

app = FastAPI()

# create a Prometheus counter to track the number of alerts received
alerts_received = Counter('alerts_received', 'Number of alerts received')

# define the endpoint for handling incoming alerts
@app.post('/alert')
async def alert(request: Request):
    # increment the counter
    alerts_received.inc()
    
    # get the JSON payload from the request
    data = await request.json()

    # extract the alert name and status
    alert_name = data['alerts'][0]['labels']['alertname']
    alert_status = data['alerts'][0]['status']
    print(alert_name)
    print(alert_status)
    
    # check if the alert status is firing
    if alert_status == 'firing':
        print("trigger hello_script")
        # execute the Bash script
        os.system('/home/kasidej/Documents/prometheus/webhook/hello_script.sh')
    
    return {"status": "success"}

# create an ASGI app that includes the Prometheus metrics endpoint
app.add_route("/metrics", make_asgi_app())

if __name__ == '__main__':
    uvicorn.run(app, host="10.15.11.106", port=5000)
