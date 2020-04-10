import requests
import datetime
import calendar
import json
import xlrd
import xlwt
import time


# 分割时间
def split_date(start, end):
    # 判断是否需要分割
    datetime_start = datetime.datetime.strptime(str(start), '%Y%m%d')
    datetime_end = datetime.datetime.strptime(str(end), '%Y%m%d')
    if datetime_end - datetime_start > datetime.timedelta(days=31):
        # 需要分割
        result = []
        first_day_week_day, month_range = calendar.monthrange(datetime_start.year, datetime_start.month)
        print(month_range)
        last_day = datetime.datetime(year=datetime_start.year, month=datetime_start.month, day=month_range)
        print(last_day)
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
def get_api_data(stations, start, end, data_type=0, scale=1):
    date_list = split_date(start, end)
    print(date_list)
    workbook = xlwt.Workbook()
    for station in stations:
        sheet = workbook.add_sheet(station)
        json_all = []

        for date_range in date_list:
            params = {
                'server': '心知',
                'station': station,
                'start_time': date_range[0],
                'end_time': date_range[1],
                'data_type': data_type,
                'scale': scale,
                'echarts': 0
            }
            url = f'http://114.67.97.73:5010/api/aqi/'
            r = requests.get(url, params)
            json_file = json.loads(r.text)['obs']
            json_all.extend(json_file)
            time.sleep(1)

        ll = list(json_all[0].keys())
        for i in range(0, len(ll)):
            sheet.write(0, i, ll[i])
        for j in range(0, len(json_all)):
            m = 0
            ls = list(json_all[j].values())
            for k in ls:
                sheet.write(j + 1, m, k)
                m += 1

    workbook.save('data.xls')


if __name__ == '__main__':
    get_api_data(['南京','北京'], 20200401, 20200420)
