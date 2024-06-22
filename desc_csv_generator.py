import csv
import pandas as pd
import copy

PRODUCT_CARE_TEMPLATE = '''
<h3>手入れ方法<br>
</h3>
<p>{{{PRODUCTCARE}}}</p>
'''

outfile = 'gbh_products_home_desc_import.csv'
shopify_export_file = '/Users/taro/Downloads/gbh_products_home.csv'

product_name_map = {'【商品情報確認中】GBH HOME TOOTHPASTE': 'GBH HOME TOOTHPASTE 0'}

df = pd.read_csv(
    '/Users/taro/Downloads/GBH product descriptions - HOME (3).csv')
df['商品名'] = df['商品名'].apply(str.strip)
df['重さ / サイズ'] = df['重さ / サイズ'].apply(lambda x: x.replace('：', ': ').replace(' : ', ': '))
df['サイズ'] = df['サイズ'].apply(lambda x: None if x == '-' else x)
df = df.drop_duplicates()

# Sort by 商品名 then サイズ
# Define a custom sorting key for サイズ
def custom_sort_key(size):
    if size == 'S':
        return (0, size)
    elif size == 'M':
        return (1, size)
    elif size == 'L':
        return (2, size)
    elif size is None:
        return (4, '')  # None values should come last
    else:
        return (3, size)  # Other values are sorted alphabetically

# Sort by 商品名 then サイズ using the custom sort key
df = df.sort_values(['商品名', 'サイズ'], key=lambda col: col.map(custom_sort_key))

# Group by 商品名
df = df.groupby('商品名').agg({'商品説明': 'first',
                              '手入れ方法': 'first',
                              '重さ / サイズ': lambda x: '\n'.join(w.replace(' : ', ': ') if not s or w.startswith(s) else f'{s}: {w}' for s, w in zip(df.loc[x.index, 'サイズ'], x.dropna())),
                              '素材': 'first',
                              '原産国': 'first'})
df = df.reset_index()
df = df.drop_duplicates()

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
    res = res.replace('{{{DESCRIPTION}}}', (descf['商品説明'] or '').replace('\n', '<br>'))
    if descf['手入れ方法']:
        product_care = PRODUCT_CARE_TEMPLATE.replace('{{{PRODUCTCARE}}}',
                                                     descf['手入れ方法'].replace('\n', '<br>'))
    else:
        product_care = ''
    res = res.replace('{{{PRODUCTCARE}}}', product_care)
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
            descf = df.loc[df['商品名'] == product_name_map.get(
                row['Title'], row['Title'])]
            print(f"processing {row['Title']}")
            desc = populate_desc(descf)
            of.write(f'{handle},{title},{desc}\n')

            
