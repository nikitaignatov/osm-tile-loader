import math
import requests
from io import BytesIO
from PIL import Image
import os

class Point:
  lat:float
  lon:float
  
  def __init__(self, lat, lon) -> None:
      self.lat = lat
      self.lon = lon
      

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def deg2num(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0**zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(x, y, zoom):
    n = 2.0**zoom
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def get_images_from_server(
    server: str, a:Point,b:Point,
    zoom: int
):
    xmin, ymax = deg2num(a.lat, a.lon, zoom)
    xmax, ymin = deg2num(b.lat, b.lon, zoom)
    img = Image.new("RGB", ((xmax - xmin + 1) * 256 - 1, (ymax - ymin + 1) * 256 - 1))
    mkdir(f"tiles/{zoom}")
    for xtile in range(xmin, xmax + 1):
        mkdir(f"tiles/{zoom}/{xtile}")
        for ytile in range(ymin, ymax + 1):
            url = f"{server}/tile/{zoom}/{xtile}/{ytile}.png"
            try:
                print(f"loading: {url}")
                imgstr = requests.get(url)
                tile = Image.open(BytesIO(imgstr.content))
                img.paste(tile, box=((xtile - xmin) * 256, (ytile - ymin) * 255))
                tile.save(f"tiles/{zoom}/{xtile}/{ytile}.png", "PNG")
            except Exception as e:
                print(f"error when loading {url} Details: {e}")
                tile = None
    return img
