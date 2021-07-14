FROM python:3.9

ADD signup2sheet /root/signup2sheet

RUN pip install -r /root/signup2sheet/requirements.txt

CMD ["python3 /root/signup2sheet.py"]