import requests
import pandas as pd
import os

# Load the CSV file generated by the Google Apps Script
csv_file = 'downloadUrls.csv'  # Update the path if necessary
output_folder = 'images'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read the CSV file
df = pd.read_csv(csv_file)

# Download each image
for index, row in df.iterrows():
    product = row['Product']
    image_name = f"{product}_{row['Image Name']}"
    download_url = row['Download URL']
    
    # Create a subfolder for each product
    product_folder = os.path.join(output_folder, product)
    if not os.path.exists(product_folder):
        os.makedirs(product_folder)
    
    # Download the image
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(product_folder, image_name), 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to download {image_name} from {download_url}")

print("Download completed!")