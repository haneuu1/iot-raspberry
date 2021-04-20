import MySQLdb
import traceback
from datetime import datetime
from django import db

class DataDAO:
    def __init__(self):
        self.host = "172.30.1.116" # 라즈베리파이 ip - database
        self.username = "root"
        self.password = "0000"
        self.databases = "iot_db"

        # mqtt 데이터
        self.timestamp = None
        self.topic = None
        self.msg = None
        
        # recording 데이터
        self.video_timestamp = None
        self.video_root = None

    def get_conn(self):
        db = MySQLdb.connect(user=self.username, host=self.host, passwd=self.password, db=self.databases)
        return db
    
    def get_cursor(self, connection):
        return connection.cursor()

    # mqtt 데이터
    def insert_data(self, topic, msg):
        self.topic = topic
        self.msg = msg
        self.timestamp = datetime.now()
        con = self.get_conn()
        cursor = self.get_cursor(con)

        query = """
        INSERT INTO mqtt_mqttdata(timestamp, topic, msg) VALUES(%s, %s, %s)
        """
        
        # print(f"{self.topic}, {self.msg}")
        
        try:
            cursor.execute(query, (self.timestamp.strftime("%Y-%m-%d %H:%M:%S"), self.topic, self.msg))
            con.commit()

        except Exception as e:
            print(traceback.format_exc())
            cursor.close()
        
        finally:
            cursor.close()
            self.topic = None
            self.msg = None

    # recording 데이터
    def insert_recording_data(self, video_timestamp, video_root):

        self.video_timestamp = video_timestamp
        self.video_root = video_root

        con = self.get_conn()
        cursor = self.get_cursor(con)

        query = """
        INSERT INTO recording_recordingdata(video_timestamp, video_root) VALUES(%s, %s)
        """
  
        try:
            cursor.execute(query, (self.video_timestamp.strftime("%Y-%m-%d %H:%M:%S"), self.video_root))
            con.commit()

        except Exception as e:
            print(traceback.format_exc())
            cursor.close()
        
        finally:
            cursor.close()

            self.video_timestamp = None
            self.video_root = None

    def get_db_data(self, topic):

        self.topic = topic
        datas = []
        con = self.get_conn()
        cursor = self.get_cursor(con)
        print('access to db')
        query = "SELECT * FROM mqtt_mqttdata WHERE topic = %s"

        try:
            cursor.execute(query, [self.topic])
            res = cursor.fetchall() 
            for data in res: 
                datas.insert(0, data)
            con.commit()
            return datas

        except Exception as e:
            print(traceback.format_exc())
            cursor.close()
        
        finally:
            cursor.close()
            self.topic = None
    
    
# if __name__ == "__main__":
#     d = DataDAO()
#     d.insert_data('topic', 'msg')
