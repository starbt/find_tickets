### 项目简介
用 Python 写一个命令行版的火车票查看器， 只要在命令行敲一行命令就能获得你想要的火车票信息.

### 安装
#### 此项目基于python3, ubuntu16.04
安装所需的库：
```
pip3 install requests 
pip3 install prettytable 
pip3 install docopt 
pip3 install colorama
```
1. requests，使用 Python 访问 HTTP 资源的必备库。
2. docopt，Python3 命令行参数解析工具。
3. prettytable， 格式化信息打印工具，能让你像 MySQL 那样打印数据。
4. colorama，命令行着色工具

### 运行
```
python3 tickets.py [参数] from_station to_station date
如： python3 ticket.py 深圳 广州 2017-10-11
```
#### 结果如下
![](https://github.com/starbt/find_tickets/raw/master/show.png)
