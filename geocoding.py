#!/usr/bin/env python3


import sys

import pandas as pd
import requests

def main(path):
    lat_list = []
    lon_list = []
    df = pd.read_csv(path, index_col=0)
    index_len = df.shape[0]
    cnt = 0
    print('[notice] Started Geocoding.')
    print(f'[notice] The estimated time is {round(0.4 * index_len, 0)} sec')
    for index, row in df.iterrows():
        cnt += 1
        lat_lon = geocoding(row.address)
        lat_list.append(lat_lon[0])
        lon_list.append(lat_lon[1])
        progress_rate = round(((cnt / index_len) * 100), 2)
        bar_num = int(int(progress_rate) / 5)
        progress_bar = '==' * bar_num + '--' * (20 - bar_num)
        sys.stdout.write(f'\r{progress_bar} {progress_rate}%')
        sys.stdout.flush()
    print('[notice] Geocoding has been finished!')
    df['lat'] = lat_list
    df['lon'] = lon_list
    df.to_csv(path.replace('_res.csv', '_geoco.csv'))


def geocoding(address):
    url = f'https://xxxxxxxxx?address={address}&key=[YOUR_KEY]'
    res = requests.get(url).json()
    try:
        loc = res['results'][0]['geometry']['location']
    except IndexError:
        loc = {'lat':'-', 'lng':'-'}
    lat = loc['lat']
    lon = loc['lng']
    return lat, lon


if __name__ == '__main__':
    main([CSV_FILE_INCLUDING_THE_ADDRESS_COLUMN])
