#From https://docs.microsoft.com/en-us/azure/azure-monitor/platform/data-collector-api
import json
import requests
import datetime
import hashlib
import hmac
import base64
import time
import datetime
import sys
import signal

run = True
#Read Settings from JSON file
try:
    f = open('/var/www/html/py/conf.json', 'r')
    config = json.load(f)
    f.close()

    # Update the customer ID to your Log Analytics workspace ID
    customer_id = config["WorkspaceId"]
    # For the shared key, use either the primary or the secondary Connected Sources client authentication key   
    shared_key = config["WorkspaceKey"]
    # The log type is the name of the event that is being submitted
    log_type = config["LogName"]
    LoopDelay = config["LogFrequency"]
except Exception as e:
    now = datetime.datetime.now()
    print(e)
    f = open('/var/www/html/python_errors.log', 'a')
    f.write("%s - AZURE - %s\n" % (now.strftime("%Y-%m-%d %H:%M:%S"), e))
    f.close()

#####################
######Functions######  
#####################

# Build the API signature
def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash).encode('utf-8')  
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest())
    authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
    return authorization

# Build and send a request to the POST API
def post_data(customer_id, shared_key, body, log_type):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri,data=body, headers=headers)

def OnKill(signum, frame):
    global run
    run = False

signal.signal(signal.SIGINT, OnKill)
signal.signal(signal.SIGTERM, OnKill)

while run:
    try:
        #Read Current Data Points
        f = open('/var/www/html/py/data.json', 'r')
        data = json.load(f)
        f.close()

        body = json.dumps(data)

        post_data(customer_id, shared_key, body, log_type)
    except Exception as e:
        now = datetime.datetime.now()
        print(e)
        f = open('/var/www/html/python_errors.log', 'a')
        f.write("%s - AZURE [%i] - %s\n" % (now.strftime("%Y-%m-%d %H:%M:%S"), sys.exc_info()[-1].tb_lineno, e))
        f.close()
    time.sleep(LoopDelay)

now = datetime.datetime.now()
f = open('/var/www/html/python_errors.log', 'a')
f.write("%s - AZURE [0] - Exit called by Interface\n" % (now.strftime("%Y-%m-%d %H:%M:%S")))
f.close()