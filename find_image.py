import json
import hashlib
from PIL import Image
import piexif
import boto3
import requests
import os
from itertools import islice


def check_missing_image(img_hash, file, alias):
    amazon_uri = 'your aws uri'
    hi_uri = amazon_uri + 'styles/project_image_high/s3/externals/' + img_hash
    med_uri = amazon_uri + 'styles/project_image_medium/s3/externals/' + img_hash

    session = boto3.Session(
        aws_access_key_id='your aws key id',
        aws_secret_access_key='your aws secret access key',
    )
    s3 = boto3.resource('s3')

    if requests.head(hi_uri).status_code != 200 or requests.head(med_uri).status_code != 200:
        print("image missing: " + img_hash)
        s3.meta.client.download_file('your aws uri', 'externals/'+file, '/Users/DEVI/Documents/project/image/'+alias+'_'+file)


def find_image():
    with open("/rotate-correction/static/active_projects.json") as f:
        data = json.load(f)

    x = 0
    y = 0
    for item in islice(data, x, len(data)):
        amazon_uri = 'your aws uri'
        img_uri = amazon_uri + item['path']
        img_hash = hashlib.md5(img_uri.encode()).hexdigest() + '.' + ('jpg' if item['ext'] == '' else item['ext'].lower())
        ext_uri = amazon_uri + 'externals/' + img_hash
        hi_uri = amazon_uri + 'styles/project_image_high/s3/externals/' + img_hash
        med_uri = amazon_uri + 'styles/project_image_medium/s3/externals/' + img_hash

        print(str(x) + ": project " + item['project_name'])

        x = x+1
        session = boto3.Session(
            aws_access_key_id='your aws key id',
            aws_secret_access_key='your aws secret access key',
        )
        s3 = boto3.resource('s3')

        response = requests.head(ext_uri)
        if response.status_code != 200:
            print(ext_uri)
            print('file not found')
            y = y+1
        else:
            img = Image.open(requests.get(ext_uri, stream=True).raw)
            file = ext_uri.split('/')[-1]
            if "exif" in img.info:
                exif_dict = piexif.load(img.info["exif"])
                if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                    orientation = exif_dict["0th"][274]
                    if orientation is not 1:
                        # orientation is wrong
                        # download externals cache image
                        print("image_rotation rotate image line 38")
                        s3.meta.client.download_file('your aws uri', 'externals/'+file, '/Users/DEVI/Documents/image/'+item['project_alias']+'_'+file)
            #         else:
            #             check_missing_image(img_hash,file,item['project_alias'])
            #     else:
            #         check_missing_image(img_hash,file,item['project_alias'])
            # else:
            #     check_missing_image(img_hash,file,item['project_alias'])


if __name__ == '__main__':
    find_image()
