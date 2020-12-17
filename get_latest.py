import requests
import datetime
import calendar
import json
import xlrd
import xlwt
import time
import pandas as pd


# 分割时间
def split_date(start, end):
    # 判断是否需要分割
    datetime_start = datetime.datetime.strptime(str(start), '%Y%m%d')
    datetime_end = datetime.datetime.strptime(str(end), '%Y%m%d')
    if datetime_end - datetime_start > datetime.timedelta(days=31):
        # 需要分割
        result = []
        first_day_week_day, month_range = calendar.monthrange(datetime_start.year, datetime_start.month)
        last_day = datetime.datetime(year=datetime_start.year, month=datetime_start.month, day=month_range)
        result.append([datetime_start.strftime('%Y%m%d'), last_day.strftime('%Y%m%d')])
        while datetime_end - last_day > datetime.timedelta(days=30):
            first_day = last_day + datetime.timedelta(days=1)
            first_day_week_day, month_range = calendar.monthrange(first_day.year, first_day.month)
            last_day = datetime.datetime(year=first_day.year, month=first_day.month, day=month_range)
            result.append([first_day.strftime('%Y%m%d'), last_day.strftime('%Y%m%d')])
        if last_day != datetime_end:
            result.append([(last_day + datetime.timedelta(days=1)).strftime('%Y%m%d'), end])
        print(result)
        return result
    else:
        # 无需分割
        print([[start, end]])
        return [[start, end]]


# 获取数据
def get_api_data(stations, start, end, data_type=0, scale=0):
    stations_list = [    {
      "监测点名称": "监测站大楼",
      "城市": "丽水",
      "监测点编码": "1267A",
      "经度": 119.914,
      "纬度": 28.4514
    },
    {
      "监测点名称": "莲都小学",
      "城市": "丽水",
      "监测点编码": "1268A",
      "经度": 119.93,
      "纬度": 28.4586
    },
    {
      "监测点名称": "余庄前",
      "城市": "丽水",
      "监测点编码": "1269A",
      "经度": 119.879,
      "纬度": 28.4231
    },]

    stations = []
    for s in stations_list:
        stations.append(s['监测点编码'])

    stations_df = pd.DataFrame(stations_list)
    json_all = []
    for station in stations:
        params = {
            'server': '心知',
            'station': station,
            'start_time': start,
            'end_time': end,
            'data_type': data_type,
            'scale': scale,
            'echarts': 0
        }
        url = f'http://47.102.42.30:5010/api/aqi/'
        r = requests.get(url, params)
        json_file = json.loads(r.text)['obs']
        print(json_file)
        json_all.extend(json_file)

    result = pd.DataFrame(json_all)
    result['AQI'] = result.apply(lambda x: x.replace('-', '')).astype('float')
    # result['CO'] = result.apply(lambda x: float(x['CO']), axis=1)
    # result['NO2'] = result.apply(lambda x: float(x['NO2']), axis=1)
    # result['O3'] = result.apply(lambda x: float(x['O3']), axis=1)
    # result['O3_8H'] = result.apply(lambda x: float(x['O3_8H']), axis=1)
    # result['PM10'] = result.apply(lambda x: float(x['PM10']), axis=1)
    # result['PM2.5'] = result.apply(lambda x: float(x['PM2.5']), axis=1)
    # result['SO2'] = result.apply(lambda x: float(x['SO2']), axis=1)
    # print(result)
    # result.to_csv('福州.csv', index=False, encoding="utf_8_sig")

    writer = pd.ExcelWriter(f'{stations_list[0]["城市"]}站点日均.xlsx')
    stations_df.to_excel(writer, sheet_name='站点信息', index=False)
    result.to_excel(writer, sheet_name='站点数据', index=False)
    writer.save()

    print('Finish!')


if __name__ == '__main__':
    station_list = ['1280A', '1281A', '1282A', '1283A', '1284A', '1285A', ]
    get_api_data(station_list, 20200101, 20201216)
