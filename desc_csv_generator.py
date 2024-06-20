import csv
import pandas as pd
import copy

outfile = 'gbh_products_apparel_desc_import.csv'
shopify_export_file = '/Users/taro/Downloads/gbh_products_apparel.csv'
df = pd.read_csv(
    '/Users/taro/Downloads/GBH product descriptions - Apparel.csv')
df = df.drop_duplicates()
df['商品名'] = df['商品名'].apply(str.strip)
df['重さ / サイズ'] = df['重さ / サイズ'].apply(lambda x: x.replace('：', ': '))
TEMPLATE = None


def desc_template():
    global TEMPLATE
    if not TEMPLATE:
        with open(f'/Users/taro/sc/playground/product_description_template.txt') as f:
            TEMPLATE = f.read()
    return copy.copy(TEMPLATE)


def populate_desc(descf):
    res = desc_template()
    descf = descf.iloc[0]
    res = res.replace('{{{DESCRIPTION}}}', descf['商品説明'].replace('\n', '<br>'))
    res = res.replace('{{{PRODUCTCARE}}}',
                      descf['手入れ方法'].replace('\n', '<br>'))
    res = res.replace('{{{PRODUCTSIZE}}}',
                      descf['重さ / サイズ'].replace('\n', '<br>'))
    res = res.replace('{{{MATERIAL}}}', descf['素材'].replace('\n', '<br>'))
    res = res.replace('{{{COUNTRY}}}', descf['原産国'].replace('\n', '<br>'))
    return res


with open(shopify_export_file) as f:
    reader = csv.DictReader(f)

    with open(outfile, 'w') as of:
        of.write('Handle,Title,Body (HTML)\n')
        for row in reader:
            handle = row['Handle']
            title = row['Title']
            if not title:
                continue
            descf = df.loc[df['商品名'] == row['Title']]
            print(f"processing {row['Title']}")
            desc = populate_desc(descf)
            of.write(f'{handle},{title},{desc}\n')

            
