FROM       python:3

WORKDIR    /app

COPY       . /app/

RUN        wget https://pjreddie.com/media/files/yolov3.weights

RUN        mv yolov3.weights /app/yolo/

RUN        pip install -r requirements.txt

RUN        chmod a+x *

CMD        ["./main.py"]
