import requests
from conversions import linkProcessing
response = requests.get(linkProcessing("+79614951406", "aaa"))
print(response.headers)