
# by Shawn Graham, drawing on code by Alex Lane, and on the Azure code snippets
# see also https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/ComputerVisionQuickstart.py
#
# First make sure to install the sdk, run at terminal:
# pip install --upgrade azure-cognitiveservices-vision-computervision

# https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/python-sdk
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

import os
import sys
import csv
#import atexit

from array import array
from PIL import Image
import time

images_processed_output = ""
'''
def on_exit_close_writing_file():
    images_processed_output.close()

atexit.register(on_exit_close_writing_file)
'''
try:
    while(True):
        default_settings = input("Would you like to use the default settings? (Y is just for dev testing) Y/N: ")
        if (default_settings == "Y"):
            print("Not a valid entry for settings")
            continue
        elif (default_settings == "N"):
            directory_of_images_filepath = input("Please enter the directory path: ")
            directory_of_images = os.fsencode(directory_of_images_filepath)

            image_filetypes = []
            while(True):
                file_type_to_add = input("Please enter a image type to search for (.png, .jpg, etc.): ")
                image_filetypes.append(file_type_to_add)
                choose_another = True
                while(True):
                    add_another_type = input("Would you like to add another file type to search for? Y/N: ")
                    if (add_another_type == "Y"):
                        break
                    elif (add_another_type == "N"):
                        choose_another = False
                        break
                    else:
                        print("Not a valid entry for settings")
                        continue
                if(choose_another == False):
                    break
            output_file_name = input("Specify a name for the output file: ")

            while(True):
                pick_directory = input("Would like to specify a directory path for the output .txt file? Otherwise, the file will be created in the same directory as this script. Y/N: ")
                if (pick_directory == "Y"):
                    output_directory = input("Please enter the output directory path: ")
                    images_processed_output = open(output_directory + output_file_name + ".txt", mode='w')
                    break
                elif (pick_directory == "N"):
                    images_processed_output = open(output_file_name + ".txt", mode='w')
                    break
                else:
                    print("Not a valid entry for settings")
                    continue
            break
        else:
            print("Not a valid entry for settings")
            continue

    image_output_writer = csv.writer(images_processed_output)

    """## Now we connect up with Azure"""

    # you have to sign up for a free trial with azure, https://portal.azure.com
    # then make a resource under 'cognitive resources'
    # for computer vision to get the correct api, endpoint
    os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']='xxxx'
    os.environ['COMPUTER_VISION_ENDPOINT']='yyyy'

    # Add your Computer Vision subscription key to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    # Add your Computer Vision endpoint to your environment variables.
    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    else:
        print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


    for image in os.listdir(directory_of_images):

        image_name = os.fsdecode(image)

        for suffix in image_filetypes:
            if (image_name.endswith(suffix)):
                '''
                Extracting tags from image, then print results, line by line.
                '''
                print("===== Processed Image - '" + image_name + "' =====")
                image_output_writer.writerow(["===== Processed Image - '" + image_name + "' ====="])
                # Get an image with printed text
                local_image = open(directory_of_images_filepath + image_name, 'rb')

                tags_result_local = computervision_client.tag_image_in_stream(local_image)

                # Print results with confidence score
                print("Tags in the local image: ")
                if (len(tags_result_local.tags) == 0):
                    print("No tags detected.")
                    image_output_writer.writerow("no tags detected")
                else:
                    for tag in tags_result_local.tags:
                        print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
                        print()
                        image_output_writer.writerow([image_name, tag.name, tag.confidence * 100])
                break
            else:
                continue

    images_processed_output.close()
except KeyboardInterrupt:
    try:
        images_processed_output.close()
        sys.exit()
    except:
        sys.exit()
