from lxml import etree
from tool import openlink
import datetime
class Crawl():
    def parse(self, html, hotel_id, hotel_name, start_date, dep_date):
        try:
            detail = []
            if html:
                tree = etree.HTML(html)
                roomlist_raw = tree.xpath('//tr')
                room_dict = {}
                crawl_time=str(datetime.datetime.now().date())
                for r in roomlist_raw:
                    room_type = ''.join(r.xpath('.//a[@class="room_unfold J_show_room_detail"]//text()')).replace('查看详情',
                                                                                                                  '').strip()
                    if room_type:
                        room_dict[r.xpath("string(@brid)")] = room_type
                    if r.xpath('@brid') and 'tr-recommend' not in r.xpath('string(@class)'):
                        if '标准价' in r.xpath('string(.//span[@class="room_type_name"])') or '提前' in \
                                r.xpath('string(.//span[@class="room_type_name"])'):
                            if '代理' not in r.xpath('string(.//span[@class="label_onsale_blue"])'):
                                detail_info = {}
                                detail_info.setdefault('brid', r.xpath('string(@brid)'))
                                detail_info.setdefault('room_id',
                                                       r.xpath('string(./td[contains(@class,"J_Col_RoomName")]/@data-roomid)'))
                                detail_info.setdefault('hotel_id', hotel_id)
                                detail_info.setdefault('hotel_name', hotel_name)
                                detail_info.setdefault('price_type', r.xpath('string(.//span[@class="room_type_name"])'))
                                detail_info.setdefault('room_type', room_dict[r.xpath("string(@brid)")])
                                detail_info.setdefault('bed_type', r.xpath('string(./td[contains(@class,"col3")])'))
                                detail_info.setdefault('breakfast_type', r.xpath('string(./td[contains(@class,"col4")])'))
                                detail_info.setdefault('price', r.xpath(
                                    'string(./td[contains(@class,"J_Col_RoomName")]/@data-pricedisplay)'))
                                detail_info.setdefault('pay_type', r.xpath('string(.//span[@class="payment_txt"])'))
                                detail_info.setdefault('start_time', start_date)
                                detail_info.setdefault('dep_date', dep_date)
                                detail_info.setdefault('crawl_time',crawl_time)
                                if r.xpath('string(.//div[@class="hotel_room_last"])'):
                                    detail_info.setdefault('room_last', r.xpath('string(.//div[@class="hotel_room_last"])'))
                                elif r.xpath('string(.//div[@class="btns_base22_main"])') == '订完':
                                    detail_info.setdefault('room_last', '无房')
                                    detail_info['price']='0'
                                else:
                                    detail_info.setdefault('room_last', '')
                                detail.append(detail_info)
            return detail
        except Exception as e:
            print(e)
            return []

    def get_hotel_name(self,hotel_id):
        try:
            hotel_name,city= openlink('http://hotels.ctrip.com/Domestic/ShowHotelInformation.aspx?hotel=%s' % hotel_id,
                             type=1)
            return hotel_name,city
        except Exception as e:
            print(e)

    def get_detail_info(self, hotel_id, start_date, dep_date,eleven):
        """
        得到酒店的具体信息
        :param hotel_id: 酒店id
        :param start_date: 入住时间
        :param dep_date: 退房时间
        :param lock: 线程锁
        :return:
        """
        headers = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
            'Host': "hotels.ctrip.com",
            'If-Modified-Since': "Thu, 01 Jan 1970 00:00:00 GMT",
            'Referer': "http://hotels.ctrip.com/domestic/hotel/%s.html?isFull=F"%hotel_id,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            'Postman-Token': "3aa8586c-caee-45a7-8cfd-5d2cbee1df43",
         } 
       
        hotel_name,city=self.get_hotel_name(hotel_id)
        info_url = "http://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx"
        filter_str="pay|1,2"
        querystring = {"psid": "", "MasterHotelID": "%s" % hotel_id, "hotel": "%s" % hotel_id, "EDM": "F", "roomId": "",
                       "IncludeRoom": "", "city": "%s" % city, "showspothotel": "T", "supplier": "",
                       "IsDecoupleSpotHotelAndGroup": "F",
                       "contrast": "0", "brand": "0", "startDate": "%s" % start_date, "depDate": "%s" % dep_date,
                       "IsFlash": "F", "RequestTravelMoney": "F",
                       "hsids": "", "IsJustConfirm": "", "contyped": "0", "priceInfo": "-1", "equip": "",
                       "productcode": "", "couponList": "", "esfiltertag": "", "estagid": "", "Currency": "",
                       "Exchange": "","filter":filter_str,'promotionf':'null,',
                       "abForHuaZhu": "", "defaultLoad": "F", "TmFromList": "F", "RoomGuestCount": "1,1,0",
                       "eleven": "%s" % eleven}
        payload = '''psid=&MasterHotelID=%s&hotel=%s&EDM=F&roomId=&IncludeRoom=&city=%s
        &showspothotel=T&supplier=&IsDecoupleSpotHotelAndGroup=F&contrast=0&brand=&startDate=%s
        &depDate=%s&IsFlash=F&RequestTravelMoney=F&hsids=&IsJustConfirm=&contyped=0&priceInfo=-1
        &equip=&filter=%s&productcode=&couponList=&abForHuaZhu=&defaultLoad=F&TmFromList=F&esfiltertag=&estagid=&Currency=&Exchange=
        &RoomGuestCount=1,1,0&promotionf=null,&eleven=%s''' % ( hotel_id, hotel_id, city, start_date, dep_date,filter_str, eleven)
      
        html = openlink(info_url,params=querystring,type=0, headers=headers)['html']
        return self.parse(html, hotel_id, hotel_name, start_date, dep_date)



