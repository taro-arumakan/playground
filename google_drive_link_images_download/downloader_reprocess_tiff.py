import os
import glob
import pandas as pd
import requests

category = 'home'
output_folder = f'/Users/taro/sc/playground/images_gbh_{category}'

def filter_dataframe(df):
  df = df[df['Image Name'].notnull()]
  df = df[df['Image Name'].str.endswith('.tif')]
  return df

def seq_from_name(name):
    seq = name.rsplit('/', 1)[-1].split('_')[-1]
    if seq.startswith('a.'):
        return -2
    if seq.startswith('b.'):
        return -1
    return int(seq.rsplit('.', 1)[0].rsplit('_', 1)[-1])
    
def get_last_sequence(product):
    names = glob.glob(f'{output_folder}/{category}_{product}*')
    names = sorted(names, key=seq_from_name)
    return seq_from_name(names[-1])

def get_output_image_name(product, image_name):
    # Function to determine the output image name
    if image_name in ['a.tif', 'b.tif']:
        return f'{category}_{product}__{image_name}'
    seq = get_last_sequence(product) + 1
    return f'{category}_{product}_{seq:02}.tif'

df = filter_dataframe(pd.read_csv(
    '/Users/taro/Downloads/productionDownloadUrls_gbh_home.csv'))

df2 = filter_dataframe(pd.read_csv(
    '/Users/taro/Downloads/productionDownloadUrls_gbh_home_2.csv'))


df = pd.concat([df, df2])

for index, row in df.iterrows():
    product = row['Product']
    image_name = row['Image Name']
    download_url = row['Download URL']

    print(f'processing {product}, {image_name}')

    # Download the image
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        output_image_name = get_output_image_name(product, image_name)
        with open(os.path.join(output_folder, output_image_name), 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to download {image_name} from {download_url}")

print("Download completed!")
