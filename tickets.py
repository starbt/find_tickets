#coding:utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都    南京    2016-10-10

"""
from docopt import docopt
from stations import stations
from prettytable import PrettyTable
from colorama import init, Fore
import requests

init()

class TrainCollection:
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, trains_result, options):
        self.trains_result = trains_result
        self.options = options
        self.code_dict = {v:k for k, v in stations.items()}

    @property
    def trains(self):
        for raw_train in self.trains_result:
            data_list = raw_train.split('|')
            train_no = data_list[3]
            initial = train_no.lower()
            if not self.options or initial in self.options:
                #出发站
                from_station_code = data_list[6]
                from_statio_name = self.code_dict[from_station_code]
                #终点站
                to_station_code = data_list[7]
                to_station_name = self.code_dict[to_station_code] 
                #时间
                start_time = data_list[8]
                arrive_time = data_list[9]
                time_cost = data_list[10]
                time_cost = time_cost.replace(':', '小时') + '分'
                if time_cost.startswith('00'):
                    time_cost = time_cost[4:]
                elif time_cost.startswith('0'):
                    time_cost = time_cost[1:]

                #座位
                first_class_seat = data_list[31] or '--'
                second_class_seat = data_list[30] or '--'
                soft_sleep = data_list[23] or '--'
                hard_sleep = data_list[28] or '--'
                hard_seat = data_list[29] or '--'
                no_seat = data_list[26] or '--'

                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + from_statio_name + Fore.RESET, 
                               Fore.RED + to_station_name + Fore.RESET]),
                    '\n'.join([Fore.GREEN + start_time + Fore.RESET,
                               Fore.RED + arrive_time + Fore.RESET]),
                    time_cost,
                    first_class_seat,
                    second_class_seat,
                    soft_sleep,
                    hard_sleep,
                    hard_seat,
                    no_seat,
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)



def cli():
    """"command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    #构建url
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&'\
      'leftTicketDTO.from_station={}&' \
      'leftTicketDTO.to_station={}&' \
      'purpose_codes=ADULT'.format(date, from_station, to_station)

    options = ''.join([key for key, value in arguments.items() if value is True])

    r = requests.get(url, verify=False)
    result = r.json()['data']['result']
    TrainCollection(result, options).pretty_print()

if  __name__ == '__main__':
    cli()
