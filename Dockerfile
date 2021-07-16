FROM python:3.9

ADD signup2sheet /root/signup2sheet

RUN pip install -r /root/signup2sheet/requirements.txt

WORKDIR /root/signup2sheet

CMD ["python3", "signup2sheet.py"]