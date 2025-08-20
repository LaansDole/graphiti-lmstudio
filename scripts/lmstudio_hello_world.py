import requests
import json
 
url = "https://sset-localai.ngrok.io/v1/chat/completions"
headers = {"Content-Type": "application/json"}
 
data = {
    "model": "openai/gpt-oss-20b",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ]
}
 
response = requests.post(url, headers=headers, data=json.dumps(data))
 
print(response.status_code)
print(response.json())