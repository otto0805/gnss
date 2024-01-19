import serial
import pynmea2
import json
from datetime import datetime

# set serial port and baudrate
port = 'COM5'  # serial port
baudrate = 9600  # baudrate of the receiver

# formatting serial port
ser = serial.Serial(port, baudrate)

# list for the result
sensor_data = []
# counter
gnrmc_cnt = 0
cnt_num = 10

# data receive and analysis
while True:
    try:
        data = ser.readline().decode('utf-8')  # read NMEA data
        
        if data.startswith('$GPRMC'):  # GNRMCセンテンスの処理
            msg = pynmea2.parse(data)
            status = msg.status  # ステータス (A: 有効、V: 無効)
            gnrmc_cnt += 1
            
        elif data.startswith('$GPGGA'):  # 例: GPGGAセンテンスの処理
            msg = pynmea2.parse(data)
            lat_dir = msg.lat_dir
            latitude = msg.latitude  # 緯度
            longitude = msg.longitude  # 経度
            lon_dir = msg.lon_dir
            altitude = msg.altitude  # 高度
            hdop = msg.horizontal_dil  # 水平精度 (HDOP)
            time = msg.timestamp  # 時刻
            time = datetime.combine(datetime.today().date(), time)
        
        # カウンタ値が所定値になったら
        if gnrmc_cnt >= cnt_num:
            gnrmc_cnt =0
            # センサーデータを辞書として作成
            sensor_datum = {
                "timestamp": datetime.now().isoformat(),
                "latitude": latitude,
                "lat_dir":lat_dir,
                "longitude": longitude,
                "lon_dir":lon_dir,
                "altitude": altitude,
                "hdop": hdop,
                "Status": status
            }
            
            # センサーデータをリストに追加
            sensor_data.append(sensor_datum)
            
            # 他の属性も利用可能
            # ...
            print(f"Time:{time}")
            print(f"Latitude:{latitude}")
            print(f"lat_dir:{lat_dir}")
            print(f"Longitude:{longitude}")
            print(f"lon_dir:{lon_dir}")
            print(f"Altitude:{altitude}")
            print(f"hdop:{hdop}")            
            print(f"Status:{status}")

            # data.jsonにセンサーデータを書き込み
            with open('data.json', 'w') as file:
                json.dump(sensor_data, file, indent=2)
            
    except KeyboardInterrupt:
        break


ser.close()