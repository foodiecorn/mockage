FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./main.py .

RUN mkdir /etc/mockage
COPY ./mockage.json /etc/mockage/

EXPOSE 5000

CMD [ "python", "./main.py" ]
