FROM python:3.10
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN pip3 install --upgrade pip

WORKDIR /var/rms-collector/rms_cctv_collector_test
ADD . /var/rms-collector/rms_cctv_collector_test
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python", "app/main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]