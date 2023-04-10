import base64
from google.cloud import aiplatform as aip
from flask import Flask, jsonify, request, send_file
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    PROJECT_NAME = 'YOUR-PROJECT-ID'
    REGION = 'us-central1'
    ENDPOINT_ID = 'YOUR-ENDPOINT-ID'
    
    # Get the input data from the HTTP request
    input_data = request.get_json()

    # Extract the text parameter from the input data
    prompt = input_data.get('prompt', '')

    aip.init(project=PROJECT_NAME, location=REGION)
    endpoint = aip.Endpoint(endpoint_name=ENDPOINT_ID)
    text_input = prompt

    # Invoke the Vertex AI endpoint 
    payload = {"prompt": text_input}
    response = endpoint.predict(instances=[payload])

    # Decode the image data from base64 format
    image_data = response.predictions[0]
    image_bytes = base64.b64decode(image_data)

    # Create a PIL Image object from the decoded image data
    image = Image.open(BytesIO(image_bytes))

    # Save the image to a BytesIO buffer
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)

    # Return the image file in the response
    return send_file(buffer, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
