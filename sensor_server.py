from gpiozero import MotionSensor
from flask import Flask
from datetime import datetime
import threading

pir = MotionSensor(16)

app = Flask(__name__)

count = 0
last_time = "없음"

@app.route("/")
def home():

    global count
    global last_time

    if count < 10:
        status = "한산"

    elif count < 30:
        status = "보통"

    else:
        status = "혼잡"

    return f"""
    <h1>강의실 이용 분석 시스템</h1>

    <p>감지 횟수 : {count}</p>

    <p>최근 감지 시간 : {last_time}</p>

    <p>AI 분석 결과 : {status}</p>
    """

def detect():

    global count
    global last_time

    while True:

        pir.wait_for_motion()

        count += 1

        last_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        print("감지", count)

        pir.wait_for_no_motion()

if __name__ == "__main__":

    t = threading.Thread(target=detect)

    t.daemon = True

    t.start()

    app.run(
        host="0.0.0.0",
        port=5000
    )
