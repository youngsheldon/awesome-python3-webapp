#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import mysql.connector,time,uuid
# import logging
# logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

def insert(temperature,humidity):
	conn = mysql.connector.connect(host='127.0.0.1', port = 3306, user='sheldon', password='sheldon', database='awesome')
	cursor = conn.cursor()
	m_id = next_id()
	created_at = time.time()
	cursor.execute('insert into room_weather_data (id, temperature, humidity, created_at) values (%s,%s,%s,%s)', (m_id,str(temperature),str(humidity),str(created_at)))
	# logger.info('insert rowcount = %s' % str(cursor.rowcount))
	print('rowcount = %s' % (str(cursor.rowcount)))
	# 提交事务:
	conn.commit()
	cursor.close()
	conn.close()

global count
count = 0
def on_message(client, userdata, msg):
    print('message: {}'.format(str(msg.payload,'gbk')))
    recv = str(msg.payload,'gbk').split('|')
    temperature = recv[0]
    humidity = recv[1]
    # logger.info('topic: %s data: %s %s' % (str(msg.topic,'gbk'), temperature, humidity))
    global count
    count += 1
    if count == 10:
        count = 0
        insert(temperature,humidity)

# 建立一个MQTT的客户端
client = mqtt.Client()
# 绑定数据接收回调函数
client.on_message = on_message

HOST_IP = 'localhost' # Server的IP地址
HOST_PORT = 1883 # mosquitto 默认打开端口
TOPIC_ID = 'pyespcar_basic_control' # TOPIC的ID

# 连接MQTT服务器
client.connect(HOST_IP, HOST_PORT, 60)
# 订阅主题
client.subscribe(TOPIC_ID)

# 阻塞式， 循环往复，一直处理网络数据，断开重连
client.loop_forever()
