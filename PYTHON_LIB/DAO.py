import MySQLdb
import traceback
from datetime import datetime
from django import db

class DataDAO:
    def __init__(self):
        self.host = "192.168.35.177" # 라즈베리파이 ip - database
        self.username = "root"
        self.password = "0000"
        self.databases = "iot_db"
        self.timestamp = None
        self.topic = None
        self.msg = None

    def get_conn(self):
        db = MySQLdb.connect(user=self.username, host=self.host, passwd=self.password, db=self.databases)
        return db
    
    def get_cursor(self, connection):
        return connection.cursor()

    def insert_data(self, topic, msg):
        self.topic = topic
        self.msg = msg
        self.timestamp = datetime.now()
        con = self.get_conn()
        cursor = self.get_cursor(con)

        query = """
        INSERT INTO mqtt_mqttdata(timestamp, topic, msg) VALUES(%s, %s, %s)
        """
        
        print(f"{self.topic}, {self.msg}")
        
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
    
# if __name__ == "__main__":
#     d = DataDAO()
#     d.insert_data('topic', 'msg')