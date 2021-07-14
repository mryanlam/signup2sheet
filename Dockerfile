FROM python:3.9

ADD coupraidbot /root/coup

RUN pip install -r /root/coup/requirements.txt

CMD ["python3 /root/coup.py"]