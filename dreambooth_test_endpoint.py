import base64
import logging
from io import BytesIO

from google.cloud import aiplatform as aip

PROJECT_NAME = 'YOUR-PROJECT-ID'
REGION = 'us-central1'
ENDPOINT_ID = 'YOUR-ENDPOINT-ID'

aip.init(project=PROJECT_NAME, location=REGION)
endpoint = aip.Endpoint(endpoint_name=ENDPOINT_ID)
text_input = """Polar bear sitting on an iceberg"""

# Invoke the Vertex AI endpoint 
def query_endpoint(endpoint, text_input):
 payload = {"prompt": text_input}
 response = endpoint.predict(instances=[payload])
 return response

response = query_endpoint(endpoint, text_input)

with open("generated_image.jpg", "wb") as g:
    g.write(base64.b64decode(response.predictions[0]))
