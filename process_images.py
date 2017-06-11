" Processes images for use in machine learning programs "
import os
import cv2
import numpy as np
import boto3



def label_image(label):
    "Conversion to one-hot array [type_1,type_2,type_3]"
    return np.array([1 if value == label else 0 for value in TYPE_LIST])

def process_image(filename, img_size, label):
    try:
        img = cv2.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE), (img_size, img_size))
    except:
        print('\nError resizing image {} in {}'.format(img, path))
        return None
    data = (np.array(img), label_image(label))
    new_name = filename.split('.')[0]
    np.save(new_name, data)
    return '{}.npy'.format(new_name)


if __name__=='__main__':
    BUCKET = 'thinkmachine-cancer-screening'
    IMG_SIZE = 50 # Size on a side (in pixels)
    TYPE_LIST = ['Type_1', 'Type_2', 'Type_3']
    print('Starting program...')
    s3 = boto3.client('s3')
    for label in TYPE_LIST:
        print(f'Label: {label}')
        obj_list = boto3.resource('s3').Bucket(BUCKET).objects.filter(Prefix=f'train/{label}/')
        for obj_summary in obj_list:
            print(obj_summary)
            # Download image as a file
            obj_filename = obj_summary.key.split('/')[-1]
            print(obj_filename)
            if obj_filename == '': # This means we got a folder, not a file
                continue
            s3.download_file(BUCKET, obj_summary.key, obj_filename) # Downloads to root dir as 'obj_filename'
            processed_img_filename = process_image(obj_filename, IMG_SIZE, label) # Process the image, which saves it to a .npy file
            # Upload img
            if processed_img_filename is not None:
                s3.upload_file(processed_img_filename, BUCKET, f'processed/train/{label}/{processed_img_filename}')
                try:
                    os.remove(processed_img_filename)
                    os.remove(obj_filename)
                except:
                    print('Could not delete at least one of "{}", "{}"'.format(processed_img_filename, obj_filename))
