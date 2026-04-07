from gpiozero import Buzzer, DigitalInputDevice  # 부저와 디지털 입력 장치 사용
import time  # 시간 지연을 위한 모듈

bz = Buzzer(18)  # GPIO 18번 핀에 부저 연결
gas = DigitalInputDevice(17)  # GPIO 17번 핀에 가스 센서 연결

try:
    while True:  # 무한 반복 (계속 감지)
        if gas.value == 0:    # 센서 값이 0이면 (LOW) → 가스 감지됨
            print("가스 감지됨")  # 상태 출력
            bz.on()  # 부저 켜기 (경고)
        else:                 # 센서 값이 1이면 (HIGH) → 정상 상태
            print("정상")  # 상태 출력
            bz.off()  # 부저 끄기

        time.sleep(0.2)  # 0.2초마다 반복 (너무 빠른 반복 방지)

except KeyboardInterrupt:  # Ctrl + C로 프로그램 종료할 때 실행
    pass  # 아무 동작 없이 종료

bz.off()  # 프로그램 종료 시 부저 꺼짐 (안전 처리)
