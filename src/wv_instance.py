import weaviate
import requests

from api_key import wv_api_key, hf_api_key, wv_cluster_net

import json

# connect to weaviate
client = weaviate.Client(
  url="https://post-editone-m7mgp1mf.weaviate.network", 
  auth_client_secret=weaviate.AuthApiKey(api_key="2RUGjqY4n32PTJrOJh0HkXQlMI2dkBf2kBsi"),
  # url="http://localhost:8080",
  additional_headers = {
      "X-HuggingFace-Api-Key": "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"
  }
)

# define class
class_obj = {
  "class": "Question",
  "vectorizer": "text2vec-huggingface",
  "moduleConfig": {
    "text2vec-huggingface": {},
    "generative-huggingface": {}
  }
}

client.schema.create_class(class_obj)

# import data
url = "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
resp = requests.get(url)
data = json.loads(resp.text)

client.batch.configure(batch_size=100)

with client.batch as batch:
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }
        batch.add_data_object(
            data_object=properties,
            class_name="Question"
        )

