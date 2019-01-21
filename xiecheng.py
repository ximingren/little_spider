import re
import requests
from lxml import etree
from tqdm import tqdm
if __name__ == '__main__':
    with tqdm(desc='酒店',total=100) as pbar:
        for i in range(10):
            pbar.update(10)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
         'Cookie': """_RGUID=5f44f4e6-8f87-49f5-bbbd-365cab9a292a; _RSG=rdqXFQEz4z5gaYchobDzkB; _RDG=28300441337b4223d02bc1d6ebb27de70d; ASP.NET_SessionId=qfmjd1n3rilfttdfyly2k5zb; _abtest_userid=0f5a7e54-071b-42d1-8d74-90da6af7dc87; OID_ForOnlineHotel=15474684819673pcpzv1547468482633102003; _ga=GA1.2.1461144232.1547468487; _gid=GA1.2.500705091.1547468487; _RF1=14.21.179.16; GUID=09031148310181334342; MKT_Pagesource=PC; appFloatCnt=7; manualclose=1; Session=SmartLinkCode=U850042&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _jzqco=%7C%7C%7C%7C%7C1.438968180.1547479680437.1547479680437.1547479680438.1547479680437.1547479680438.0.0.0.1.1; __zpspc=9.1.1547479680.1547479680.1%234%7C%7C%7C%7C%7C%23; Union=AllianceID=16875&SID=850042&OUID=7yrZ1OKORQZ9Gxi; HotelDomesticVisitedHotels1=1413498=0,0,4.2,4496,/200a070000002iqsx18A3.jpg,&433176=0,0,4.3,2441,/20060800000032o1750F3.jpg,&425164=0,0,4.2,3341,/hotel/53000/52741/941abc93388f496cb660691cf8b48bde.jpg,; _bfa=1.1547468481967.3pcpzv.1.1547518810818.1547521179436.4.47.212094; _bfs=1.3; MKT_OrderClick=ASID=&CT=1547521248611&CURL=http%3A%2F%2Fhotels.ctrip.com%2Fdomestic%2Fhotel%2F1413498.html%3FisFull%3DF&VAL={"pc_vid":"1547468481967.3pcpzv"}; Mkt_UnionRecord=%5B%7B%22aid%22%3A%2216875%22%2C%22timestamp%22%3A1547521248620%7D%5D; _bfi=p1%3D102003%26p2%3D0%26v1%3D47%26v2%3D46""",
        'Host': 'hotels.ctrip.com',
        'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://hotels.ctrip.com/domestic/hotel/433176.html?isFull=F',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    res = requests.get(
        "http://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx?psid=&MasterHotelID=1413498&hotel=1413498&EDM=F&roomId=&IncludeRoom=&city=30&supplier=&showspothotel=T&IsDecoupleSpotHotelAndGroup=F&contrast=0&brand=0&startDate=2019-01-15&depDate=2019-01-16&IsFlash=F&RequestTravelMoney=F&hsids=&IsJustConfirm=&contyped=0&priceInfo=-1&equip=&filter=bed|0,bf|0,networkwifi|0,networklan|0,policy|0,hourroom|0,reserve|0,pay|1,2,triple|0,addbed|0,chooseroom|0,ctrip|0,hotelinvoice|0,CtripService|0&productcode=&couponList=&abForHuaZhu=&defaultLoad=F&esfiltertag=&estagid=&Currency=&Exchange=&RoomGuestCount=1,1,0&promotionf=null,&eleven=f0488141aeb3c7859ef3cb6a50ab5b03a54e84efaad4ca41e80206669ae6c953&callback=CASIgITKoJiVVUSqrYf&_=1547521852274",        headers=headers)
    print(res.text)
    print(res.json()['html'])


def usere(regex, getcontent):  # regex
    pattern = re.compile(regex)
    content = re.findall(pattern, getcontent)
    return content


def modify(string):
    '''
    add escape to special signs
    '''
    string = string.replace('(', '\(')
    string = string.replace(')', '\)')
    return string


detail_info = {}
detail = []
f = open('main.html', 'r', encoding='utf8')
html = f.read()
tree = etree.HTML(html)
hotel_name = etree.HTML(
    requests.get('http://hotels.ctrip.com/Domestic/ShowHotelInformation.aspx?hotel=433176').text).xpath(
    'string(//h2[@class="cn_n"])')
roomlist_raw = tree.xpath('//tr')
date = '2019'
# for i in roomlist_raw[0:2]:
# replaceregex = 'onNameNewClick\(this\)\\\\\">\\\\u000a%s' % modify(i)
# replacestr = usere(replaceregex, html)[0]
# html = html.replace(replacestr, '', 1)
roomlist_raw = roomlist_raw[2:]  # exclude recommendations
# roomlist = list(map(lambda x: x.strip(' '), roomlist_raw))
# roomlist_raw = list(map(lambda x: modify(x), roomlist_raw))
# splitlist = roomlist_raw[1:]
# splitlist.append('}')
# splitlist = [[i, j] for i, j in zip(roomlist_raw, splitlist)]
for r in roomlist_raw:
    if r.xpath('@brid') and 'tr-recommend' not in r.xpath('@class')[0]:
        print(r.xpath('string(.//span[@class="room_type_name"])'))
        if '标准价' in r.xpath('string(.//span[@class="room_type_name"])') or '提前' in \
                r.xpath('.//span[@class="room_type_name"]/text()')[0]:
            detail_info.setdefault('酒店名称', hotel_name)
            detail_info.setdefault('价格类型', r.xpath('string(.//span[@class="room_type_name"])'))
            detail_info.setdefault('房型', r.xpath('string(.//a[@class="room_unfold J_show_room_detail"])').strip(
                '查看详情').strip())
            detail_info.setdefault('床型', r.xpath('string(./td[contains(@class,"col3")])'))
            detail_info.setdefault('早餐类型', r.xpath('string(./td[contains(@class,"col4")])'))
            detail_info.setdefault('政策', r.xpath('string(.//span[@class="room_policy"])'))
            detail_info.setdefault('房价', r.xpath('./td[contains(@class,"J_Col_RoomName")]//@data-pricedisplay'))
            detail_info.setdefault('支付类型', r.xpath('string(.//span[@class="payment_txt"])'))
            detail_info.setdefault('时间', date)
            if r.xpath('.//div[class="hotel_room_last"]'):
                detail_info.setdefault('剩余房量', r.xpath('string(.//div[class="hotel_room_last"])'))
            elif r.xpath('string(.//div[@class="btns_base22_main"])') == '订完':
                detail_info.setdefault('剩余房量', 0)
            else:
                detail_info.setdefault('剩余房量', '')

        detail.append(detail_info)
print(detail)
for idx, split in enumerate(splitlist):
    sub_detail_info = {}
    splitregex = 'onNameNewClick\(this\)\\\\\">\\\\u000a%s([\s\S]*?)onNameNewClick\(this\)\\\\\">\\\\u000a%s' % (
        split[0], split[1])
    if idx == len(splitlist) - 1:
        splitregex = 'onNameNewClick\(this\)\\\\\">\\\\u000a%s([\s\S]*)%s' % (split[0], split[1])
    temp_html = usere(splitregex, html)[0]
    priceregex = 'base_price[\s\S]*?(\d+?)<'
    temp_price = usere(priceregex, temp_html)
    print(temp_price)
    sub_detail_info.setdefault('price', []).extend(temp_price)
    detail_info.setdefault(roomlist[idx], []).extend(temp_price)
    satisfyregex = '预订满意度[\s\S]*?([\d+%].*?)<'
    temp_satisfy = usere(satisfyregex, temp_html)
    sub_detail_info.setdefault('satisfy', []).extend(temp_satisfy)
    roomidregex = '"roomid\\\\\":\\\\\"(\d+?)\\\\\"'
    temp_roomid = usere(roomidregex, temp_html)
    fullregex = 'data-isMember([\s\S]*?)预订'
    temp_fullhtml = usere(fullregex, temp_html)
    temp_full_left = []
    for full in temp_fullhtml:
        hrefregex = "InputNewOrder.aspx\?(.*?)\\\'  onclick"
        full_domain = 'http://hotels.ctrip.com/DomesticBook/InputNewOrder.aspx?'
        full_href = full_domain + usere(hrefregex, full)[0]
        left = get_room_left(full_href)
        temp_full_left.append(left)
    sub_detail_info.setdefault('room_left', []).extend(temp_full_left)
    detail_info[roomlist[idx]] = sub_detail_info
    replaceregex = 'onNameNewClick\(this\)\\\\\">\\\\u000a%s' % split[0]
    replacestr = usere(replaceregex, html)[0]
    html = html.replace(replacestr, '', 1)
