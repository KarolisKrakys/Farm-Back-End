from flask import Flask
from flask import request
from flask_cors import CORS
import ee
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import json
import math
import requests


from calculate_area import calculate_area
app = Flask(__name__)
CORS(app)
# SERVICE_ACCOUNT = 'geodata@hackathon-342609.iam.gserviceaccount.com'
# KEY = 'keys.json'
# PROJECT = 'hackathon'
# credentials = service_account.Credentials.from_service_account_file(KEY)
# scoped_credentials = credentials.with_scopes(
#     ['https://www.googleapis.com/auth/cloud-platform'])

# session = AuthorizedSession(scoped_credentials)

# url = 'https://earthengine.googleapis.com/v1beta/projects/earthengine-public/assets/LANDSAT'
# ee_creds = ee.ServiceAccountCredentials(SERVICE_ACCOUNT, KEY)
ee.Authenticate()
ee.Initialize()
bands = ['temperature_2m', "soil_temperature_level_1", "total_precipitation", "surface_net_solar_radiation"]
b_min = [250, 250, 0, 80000]
b_max = [320,320,0.01, 25000000]
BUFFER = 10
@app.route('/img', methods =['POST'])
def get_cordinates():
    coors = request.json['coords']
    coors = list(map(float, coors))
    ld_lon, ld_lat, ru_lon, ru_lat = coors
    c_lon = (ld_lon + ru_lat) / 2
    c_lat = (ld_lat + ru_lat) / 2
    ld = (ld_lat, ld_lon)
    ru = (ru_lat, ru_lon)
    d = calculate_area(ld, ru)
    side_len = d/math.sqrt(2)
    era5 = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY')
    era5_img = era5.mean()
    

    lower_lat = ld_lat + side_len/4
    upper_lat = ld_lat + side_len*3/4

    left_lon = ld_lon + side_len/4
    right_lon = ld_lon + side_len*3/4

    arrs = [(left_lon, upper_lat), (right_lon, upper_lat), (left_lon, lower_lat), (right_lon, lower_lat)]
    pois = [ee.Geometry.Point(*p) for p in arrs]
    rois = [poi.buffer(BUFFER) for poi in pois]

    # cordinates = request.form.getlist('cords[]')
    for count, roi in enumerate(rois):
        for i, band in enumerate(bands):
            img_info = {
                'min': b_min[i],
                'max': b_max[i],
                'bands':[band],
                'dimensions': 512,
                'palette': ["000080","#0000D9","#4000FF","#8000FF","#0080FF","#00FFFF",
                "#00FF80","#80FF00","#DAFF00","#FFFF00","#FFF500","#FFDA00",
                "#FFB000","#FFA400","#FF4F00","#FF2500","#FF0A00","#FF00FF"],
                'region': roi, 
            }
            url = era5_img.getThumbUrl(img_info)
            folder_dir = band.split('_')[0]
            r = requests.get(url)
            with open(f'{folder_dir}/{count}.png', 'wb') as f:
                f.write(r.content)



if __name__ == '__main__':
    app.run()
