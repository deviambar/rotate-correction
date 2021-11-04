from PIL import Image
import piexif
import os
from itertools import islice


def generate_rotation(filename):
    img = Image.open(filename)
    exif = piexif.load(filename)

    watermark = Image.open('/Users/DEVI/Documents/new_logo_watermark.png')

    width, height = img.size   # Get dimensions
    left = (width-height)/2
    top = 0
    right = width-left
    bottom = height

    cropped_example = img.crop((left, top, right, bottom))

    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])

        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"][piexif.ImageIFD.Orientation]
            for key in exif_dict['0th'].keys():
                if key == piexif.ImageIFD.Orientation:
                    exif_dict['0th'][key] = 1

            exif_bytes = piexif.dump(exif_dict)

            if orientation == 2:
                cropped_example = cropped_example.transpose(Image.FLIP_LEFT_RIGHT)
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                cropped_example = cropped_example.rotate(180)
                img = img.rotate(180)
            elif orientation == 4:
                cropped_example = cropped_example.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                cropped_example = cropped_example.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                cropped_example = cropped_example.rotate(-90, expand=True)
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                cropped_example = cropped_example.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                cropped_example = cropped_example.rotate(90, expand=True)
                img = img.rotate(90, expand=True)

    img_h = cropped_example.resize((500,500))
    img_m = cropped_example.resize((196,196))

    filee = filename.split('/')[-1]

    ul = round((500-196)/2)
    transparent = Image.new('RGBA', (500, 500), (0,0,0,0))
    transparent.paste(img_h, (0,0))
    # transparent.paste(watermark, (ul,ul), mask=watermark)
    new = transparent.convert('RGB')
    new.save('/Users/DEVI/Documents/image/high/' + filee)

    transparent = Image.new('RGBA', (196, 196), (0,0,0,0))
    transparent.paste(img_m, (0,0))
    # transparent.paste(watermark, (0,0), mask=watermark)
    new = transparent.convert('RGB')
    new.save('/Users/DEVI/Documents/image/medium/' + filee)

def rotate():
    x = 0
    watermark = Image.open('/Users/DEVI/Documents/new_logo_watermark.png')

    project_list = list()
    data = os.listdir("/Users/DEVI/Documents/image/")
    sorteddata = sorted(data, key=str)

    x = 0
    y = len(sorteddata)
    for file in islice(sorteddata, x, y):
        if file.endswith(".jpg"):
            x = x+1
            if file.split('_')[0] not in project_list:
                project_list.append(file.split('_')[0])

            filename = os.path.join("/Users/DEVI/Documents/image/", file)
            # print('rotating image: {} {}'.format(x,filename))
            try:
                generate_rotation(filename)
            except:
                print('rotating image failed: {} {}'.format(x,filename))


    print(x)
    print(len(project_list))
    print(sorted(project_list, key=str))


if __name__ == '__main__':
    rotate()
