from PIL import Image
import requests
from io import BytesIO

requests.verify="/etc/letsencrypt/live/yourdiary.top/fullchain.pem"

url = "https://yourdiary.top/media/images/annotations/images_1.jpeg"
response = requests.get(url)
# img = Image.open(BytesIO(response.content))
print(response.content)