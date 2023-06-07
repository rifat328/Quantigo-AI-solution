import json
import os

def convert_json(filename):
    with open(filename) as f:
        data = json.load(f)

    newData = [{
        'dataset_name': os.path.basename(filename),
        'image_link': '',
        'annotation_type': 'image',
        'annotation_objects': {},
        'annotation_attributes': {}
    }]

    for obj in data['objects']:
        if obj['classTitle'] == 'Vehicle':
            newData[0]['annotation_objects']['vehicle'] = {
                'presence': 1,
                'bbox': obj['points']['exterior'][0] + obj['points']['exterior'][1]
            }
            newData[0]['annotation_attributes']['vehicle'] = {}
            for tag in obj['tags']:
                newData[0]['annotation_attributes']['vehicle'][tag['name']] = tag['value']
        elif obj['classTitle'] == 'License Plate':
            newData[0]['annotation_objects']['license_plate'] = {
                'presence': 1,
                'bbox': obj['points']['exterior'][0] + obj['points']['exterior'][1]
            }
            newData[0]['annotation_attributes']['license_plate'] = {}
            for tag in obj['tags']:
                newData[0]['annotation_attributes']['license_plate'][tag['name']] = tag['value']

    newFile = 'formatted_' + os.path.basename(filename)
    with open(newFile, 'w') as f:
        json.dump(newData, f, indent=4)
    print(f'File created: {filename} to {newFile}')

def combine_jsons():
    folder_path = os.getcwd()  # JSON files are in the current working directory

    combined_data = []
    json_files = ['pos_0.png.json', 'pos_10010.png.json', 'pos_10492.png.json']

    for json_file in json_files:
        with open(os.path.join(folder_path, json_file), 'r') as file:
            data = json.load(file)

        for obj in data['objects']:
            new_obj = {}
            if obj['classTitle'] == 'Vehicle':
                new_obj['class'] = 'car'
            elif obj['classTitle'] == 'License Plate':
                new_obj['class'] = 'number'

            new_obj['bounding_box'] = obj['points']['exterior'][0] + obj['points']['exterior'][1]
            combined_data.append(new_obj)

    combined_json = {'combined_objects': combined_data}
    combined_filename = 'combined.json'

    with open(combined_filename, 'w') as file:
        json.dump(combined_json, file, indent=4)

    print(f'Successfully combined JSON files into {combined_filename}')

# Testing:::
json_file1 = 'pos_0.png.json'
json_file2 = 'pos_10010.png.json'
json_file3 = 'pos_10492.png.json'
convert_json(json_file1)
convert_json(json_file2)
convert_json(json_file3)
combine_jsons()

# to see newly created files: originally done on jupiter notebook
with open('combined.json','r') as f:
    dataShowCombined=json.load(f)
print(dataShowCombined)
#-----------------------------------------------
with open('formatted_pos_0.png.json','r') as f:
    dataShow1=json.load(f)
print(dataShow1)
#-----------------------------------------------
with open('formatted_pos_10010.png.json','r') as f:
    dataShow2=json.load(f)
print(dataShow2)
#-----------------------------------------------
with open('formatted_pos_10492.png.json','r') as f:
    dataShow3=json.load(f)
print(dataShow3)