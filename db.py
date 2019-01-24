import pymysql
from config import *
import pandas as pd
import json

class Mysql_db():

    def __init__(self):
        self.db = self.connect_db(db_host, db_port, db_user, db_password, db_name)

    def connect_db(self, host, port, user, password, database=None, charset=None):
        return pymysql.connect(host=host, port=port, user=user, passwd=password, db=database, charset=charset)

    def insert_one(self, info):
        cur = self.db.cursor()
        try:
            query_sql = ("SELECT price FROM hotel WHERE room_id='%s' and start_time='%s'and crawl_time='%s'")
            cur.execute(query_sql % (info['room_id'], info['start_time'], info['crawl_time']))
            result = cur.fetchall()
            if result:
                result = result[0][0].split(',')
                result.append(info['price'])
                self.price_size = len(result)
                update_sql = (
                    "UPDATE hotel SET price='%s',room_condition='%s'WHERE room_id='%s' and start_time='%s' and crawl_time='%s'")
                cur.execute(update_sql % (
                ','.join(result), info['room_last'], info['room_id'], info['start_time'], info['crawl_time']))
            else:
                self.price_size = 1
                insert_sql = (
                    "INSERT INTO hotel(room_id,hotel_name,hotel_id,price_type,start_time,room_type,bed_type,breakfast_type,price,room_condition,pay_type,crawl_time)"
                    " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')")
                cur.execute(insert_sql % (
                info['room_id'], info['hotel_name'], info['hotel_id'], info['price_type'], info['start_time'],
                info['room_type'], info['bed_type']
                , info['breakfast_type'], info['price'], info['room_last'], info['pay_type'], info['crawl_time']))
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        finally:
            cur.close()

    def get_id(self):
        cur = self.db.cursor()
        try:
            query_sql = ("SELECT hotel_id FROM hotel_id")
            cur.execute(query_sql)
            result = cur.fetchall()
            return list(result)
        except Exception as e:
            print(e)
        finally:
            cur.close()

    def repair(self, hotel_id, crawl_time, start_time):
        query_sql = "SELECT price,room_id FROM hotel WHERE hotel_id='%s' and crawl_time='%s' and start_time='%s'"
        cur = self.db.cursor()
        cur.execute(query_sql % (hotel_id, crawl_time, start_time))
        result = pd.Series(cur.fetchall())
        try:
            for i in result:
                price = i[0].split(',')
                if len(price) != self.price_size:
                        price.append('0')
                        room_condition=None
                        for j in price:
                            if j!='0':
                                room_condition = '此房型没有'
                            else:
                                room_condition='无房'
                        update_sql = "UPDATE hotel SET price='%s',room_condition='%s'WHERE room_id='%s'and hotel_id='%s' and crawl_time='%s' and start_time='%s'"
                        cur.execute(update_sql % (','.join(price), room_condition, i[1], hotel_id, crawl_time, start_time))
                        self.db.commit()
                        self.db.rollback()
        finally:
            cur.close()

    def get_data(self, args):
        query_sql = "SELECT %s FROM hotel WHERE "
        args_length = len(args.keys())
        i = 0
        for key, value in args.items():
            i = i + 1
            if i == args_length:
                query_sql += ' ' + key + '="' + value + '"'
            else:
                query_sql += ' ' + key + '="' + value + '" and '
        try:
            cur = self.db.cursor()
            cur.execute(query_sql % (query_field))
            raw_data = cur.fetchall()
            result_list = []
            field = query_field.split(',')
            for i in range(len(raw_data)):
                each = {}
                for j in range(len(field)):
                    each[field[j]] = str(raw_data[i][j])
                result_list.append(each)
            result = json.dumps({'condition': 'success', 'data': result_list, 'count': len(raw_data)},
                                ensure_ascii=False)
            return result
        except Exception as e:
            return json.dumps({'condition': 'failed', 'data': [], 'count': '0'})
        finally:
            cur.close()
