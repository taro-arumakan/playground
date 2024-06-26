import os
import pandas as pd

shopify_image_root = 'https://cdn.shopify.com/s/files/1/0655/9596/5639/files'
out_products_csv_path = 'image_urls_gbh_home.csv'
image_dir = '/Users/taro/sc/playground/images_gbh_home'
df = pd.read_csv('/Users/taro/Downloads/products_export_gbh_home.csv')    # Shopify products export file


df = df[['Handle', 'Title', 'Variant SKU']]
df = df[df['Variant SKU'].notnull()]
df['Variant SKU'] = df['Variant SKU'].apply(lambda x: x[1:] if x.startswith("'") else x)

sku_images_map = {}
for n in os.listdir(image_dir):
  sku_images_map.setdefault(n.split('_')[1], []).append(n)

expanded_rows = []

title = None
for _, row in df.iterrows():
    sku = row["Variant SKU"]
    if pd.notnull(row['Title']):
        position = 1
        title = row['Title']
    if sku in sku_images_map:
        images = sku_images_map[sku]
        images.sort(key=lambda x: (-2 if x.endswith('__a.jpg') else (
                                   -1 if x.endswith('__b.jpg') else 
                                   int(x.split('_')[-1].split('.')[0])), x))
        for img in images:
            expanded_rows.append({
                "Handle": row["Handle"],
                "Title": title,
                "Image Src": f'{shopify_image_root}/{img}',
                "Image Position": position
            })
            position += 1

expanded_df = pd.DataFrame(expanded_rows)
expanded_df.to_csv(out_products_csv_path, index=False)
