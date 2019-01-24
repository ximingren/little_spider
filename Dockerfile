FROM python:3.6
RUN mkdir /code
WORKDIR /code
COPY . /code/
EXPOSE 5000
LABEL maintainer="ximingren <987327263@qq.com>"
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
