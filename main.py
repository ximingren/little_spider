import datetime
import threading
from queue import Queue
from tqdm import tqdm
from ctrip_funcs import Crawl
from db import Mysql_db
from tool import runTask, preprocess, get_eleven, MyThread
import time

def main(id,lock,q,hotel_id):
    crawl=Crawl()
    eleven=get_eleven(id)
    for i in tqdm(desc='酒店%s进度'%id[0],iterable=range(0, 7)):
        crawl_time=datetime.datetime.now().date()
        start_date =crawl_time + datetime.timedelta(days=i) #入住时间
        dep_date = str(start_date + datetime.timedelta(days=1)) #退房时间
        detailinfo = crawl.get_detail_info(id[0], str(start_date), dep_date,eleven) #获得酒店的具体信息
        result = preprocess(detailinfo) #对得到的数据进行预处理
        for i in result:
            db.insert_one(i)
       # db.repair(id[0],str(crawl_time),str(start_date))
    lock.acquire()
    q.put(q.get()+1)
    now = q.get()
    q.put(now)
    with tqdm(desc='总进度',total=len(hotel_id)) as pbar:
        pbar.update(now)
    lock.release()

def init():
    """
    进行爬虫前的准备工作
    :return:
    """
    hotel_id = db.get_id()
    # thread=[]
    q = Queue()
    q.put(0)
    lock=threading.Lock()
    for id in hotel_id:
        main(id,lock,q,hotel_id)
        #t=threading.Thread(target=main,args=(id,lock,q,hotel_id,eleven))
        #thread.append(t)
    #for t in thread:
     #   t.start()
      #  time.sleep(1)
    #for t in thread :
     #   t.join()
    
if __name__ == '__main__':
    db = Mysql_db()
    runTask(init,hour=1)
