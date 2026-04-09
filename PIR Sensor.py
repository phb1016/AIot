from gpiozero import MotionSensor      # Raspberry Pi GPIO 핀 제어를 위한 라이브러리 (모션 센서용)
import time                            # 시간 지연(sleep)을 위한 라이브러리
from picamera2 import Picamera2        # Raspberry Pi Camera 모듈 버전 2 제어 라이브러리
import datetime                        # 파일 이름에 사용할 현재 날짜와 시간을 가져오기 위한 라이브러리

# GPIO 16번 핀에 연결된 PIR 모션 센서 객체 생성
pirPin = MotionSensor(16)

# 카메라 객체 생성 및 초기 설정
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration() # 카메라 프리뷰 설정 생성
picam2.configure(camera_config)                       # 설정 적용
picam2.start()                                        # 카메라 모듈 시작

try:
    # 무한 루프를 통해 센서 상태를 지속적으로 확인
    while True:
        try:
            sensorValue = pirPin.value        # 센서의 현재 값 (움직임 감지 시 1, 아니면 0)
            
            if sensorValue == 1:              # 움직임이 감지되었을 때
                now = datetime.datetime.now() # 현재 시간 정보 획득
                print(now)                    # 콘솔창에 현재 시간 출력
                
                # 파일명을 "연-월-일 시:분:초.jpg" 형식으로 생성
                fileName = now.strftime('%Y-%m-%d %H:%M:%S')
                picam2.capture_file(fileName + '.jpg') # 사진 촬영 및 저장
                
                time.sleep(0.5)               # 0.5초 대기
        except:
            # 루프 내부에서 오류 발생 시 무시하고 진행
            pass

except KeyboardInterrupt:
    # Ctrl+C를 눌러 종료
    pass
