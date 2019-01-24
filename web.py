import datetime

from flask import Flask, request, Response

from db import Mysql_db

app=Flask(__name__)
@app.route("/")
def hello():
    db = Mysql_db()
    args=dict(request.args)
    if 'timeStamp' in args.keys():
        del args['timeStamp']
    if 'page' in args.keys():
        del args['page']
    if 'rows' in args.keys():
        del args['rows']
    for key,value in args.items():
        args[key]=value[0]
    if 'crawl_time'not in args.keys():
        args['crawl_time']=str(datetime.datetime.now().date())
    data=db.get_data(args)
    return  Response(data, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

