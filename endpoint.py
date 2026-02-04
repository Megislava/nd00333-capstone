import requests
import json

# URL for the web service
scoring_uri = 'https://hf-endpoint-af2f866d.westeurope.inference.ml.azure.com/score'
# If the service is authenticated, set the key or token
key = '422pkjcJKtzYc7uvtMGLL7k6zO2QMUj9ZanNkJU5lacqTPtRdFxAJQQJ99CBAAAAAAAAAAAAINFRAZMLvO5Z'

# Two sets of data to score, so we get two results back
data = {
    "data":
    [
        {
            "age":75,
            "anaemia":0,
            "creatinine_phosphokinase":582,
            "diabetes":0,
            "ejection_fraction":20,
            "high_blood_pressure":1,
            "platelets":265000,
            "serum_creatinine":1.9,
            "serum_sodium":130,
            "sex":1,
            "smoking":0,
            "time":4,
            "DEATH_EVENT":1
        },
        {
            "age":55,
            "anaemia":0,
            "creatinine_phosphokinase":7861,
            "diabetes":0,
            "ejection_fraction":38,
            "high_blood_pressure":0,
            "platelets":263358.03,
            "serum_creatinine":1.1,
            "serum_sodium":136,
            "sex":1,
            "smoking":0,
            "time":6,
            "DEATH_EVENT":1
        },
    ]
}
# Convert to JSON string
input_data = json.dumps(data)
with open("data.json", "w") as _f:
    _f.write(input_data)

# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Bearer {key}'

# Make the request and display the response
resp = requests.post(scoring_uri, input_data, headers=headers)
print(resp.json())


