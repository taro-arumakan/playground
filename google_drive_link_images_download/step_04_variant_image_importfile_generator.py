import pandas as pd

outfile = '/Users/taro/Downloads/variant_images.csv'
df = pd.read_csv('/Users/taro/Downloads/products_export_1-4.csv')
images = df[['Image Src']]
df = df[['Handle', 'Title', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Variant SKU', 'Variant Image']]
df = df[df['Variant SKU'].notnull()]
df['Variant SKU'] = df['Variant SKU'].apply(lambda x: x.replace("'", ''))

def image_url(sku):
    res = images[images['Image Src'].str.contains(sku)]
    if not res.empty:
        return res.iloc[0]['Image Src']

df['Variant Image'] = df['Variant SKU'].apply(image_url)
df = df.ffill()
df.to_csv(outfile, index=False)
