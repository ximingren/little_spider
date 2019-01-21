import pymysql
from config import *
import pandas as pd
class Mysql_db():
    def connect_db(self,host,port,user,password,database=None,charset=None):
        return pymysql.connect(host=host,port=port,user=user,passwd=password,db=database,charset=charset)

    def insert_one(self,info):
        db=self.connect_db(db_host,db_port,db_user,db_password,db_name)
        cur=db.cursor()
        try:
            query_sql=("SELECT price FROM hotel WHERE id='%s' and start_time='%s'and crawl_time='%s'")
            cur.execute(query_sql%(info['room_id'],info['start_time'],info['crawl_time']))
            result=cur.fetchall()
            if result:
                result=result[0][0].split(',')
                result.append(info['price'])                
                self.price_size=len(result)
                update_sql=("UPDATE hotel SET price='%s',room_last='%s'WHERE id='%s' and start_time='%s' and crawl_time='%s'")
                cur.execute(update_sql%(','.join(result),info['room_last'],info['room_id'],info['start_time'],info['crawl_time']))
                
            else:
                self.price_size=1
                insert_sql=("INSERT INTO hotel(id,hotel_name,hotel_id,price_type,start_time,room_type,bed_type,breakfast_type,price,room_last,pay_type,crawl_time)"
                         " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')")
                cur.execute(insert_sql%(info['room_id'],info['hotel_name'],info['hotel_id'],info['price_type'],info['start_time'],info['room_type'],info['bed_type']
                                           ,info['breakfast_type'],info['price'],info['room_last'],info['pay_type'],info['crawl_time']))
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            cur.close()
            db.close()
            

    def get_id(self):
        db = self.connect_db(db_host,db_port,db_user,db_password,db_name)
        cur=db.cursor()
        try:
            query_sql = ("SELECT hotel_id FROM hotel_id")
            cur.execute(query_sql)
            result=cur.fetchall()
            return list(result)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            db.close()

    def repair(self, hotel_id, crawl_time, start_time):
        query_sql = "SELECT price,id FROM hotel WHERE hotel_id='%s' and crawl_time='%s' and start_time='%s'"
        db = self.connect_db(db_host, db_port, db_user, db_password, db_name)
        cur = db.cursor()
        cur.execute(query_sql % (hotel_id, crawl_time, start_time))
        result = pd.Series(cur.fetchall())
        try:
            for i in result:
                price = i[0].split(',')
                if len(price) != self.price_size:
                    try:
                        price.append('0')
                        update_sql = "UPDATE hotel SET price='%s',room_last='%s'WHERE id='%s'and hotel_id='%s' and crawl_time='%s' and start_time='%s'"
                        cur.execute(update_sql % (','.join(price), '无房', i[1], hotel_id,crawl_time, start_time))
                        db.commit()
                    except Exception as e:
                        db.rollback()
                        print(e)
        finally:
                   cur.close()
                   db.close()
