from gpiozero import LED   # GPIO 핀으로 LED를 제어하기 위해 불러오는 라이브러리
from time import sleep      # 시간 지연(대기)을 위해 불러온 라이브러리

# LED 객체 생성 (GPIO 핀 번호 지정) 
carLedRed    = LED(2)    # 차량 신호등: 빨강 LED → GPIO 2번 핀
carLedYellow = LED(3)    # 차량 신호등: 노랑(파랑) LED → GPIO 3번 핀
carLedGreen  = LED(4)    # 차량 신호등: 초록 LED → GPIO 4번 핀
humanLedRed  = LED(20)   # 보행자 신호등: 빨강 LED → GPIO 20번 핀
humanLedGreen= LED(21)   # 보행자 신호등: 초록 LED → GPIO 21번 핀

try:
    while 1:    # 무한 루프: 신호등 패턴을 계속 반복

        # ── 1단계: 차량 초록 / 보행자 빨강 (차량 통행 허용) 
        carLedRed.value    = 0   # 차량 빨강 off
        carLedYellow.value = 0   # 차량 노랑(파랑) off
        carLedGreen.value  = 1   # 차량 초록 on
        humanLedRed.value  = 1   # 보행자 빨강 on  (보행자 대기)
        humanLedGreen.value= 0   # 보행자 초록 off
        sleep(3.0)               # 3초 유지

        # 2단계: 차량 노랑 / 보행자 빨강 (경고) 
        carLedRed.value    = 0   # 차량 빨강 off
        carLedYellow.value = 1   # 차량 노랑 on  (곧 빨강으로 바뀐다고 경고)
        carLedGreen.value  = 0   # 차량 초록 off
        humanLedRed.value  = 1   # 보행자 빨강 on  (보행자 계속 대기)
        humanLedGreen.value= 0   # 보행자 초록 off
        sleep(1.0)               # 1초 유지

        # 3단계: 차량 빨강 / 보행자 초록 (보행자 통행 허용) 
        carLedRed.value    = 1   # 차량 빨강 on  (차량 정지)
        carLedYellow.value = 0   # 차량 노랑 off
        carLedGreen.value  = 0   # 차량 초록 off
        humanLedRed.value  = 0   # 보행자 빨강 off
        humanLedGreen.value= 1   # 보행자 초록 on  (보행자 통행 허용)
        sleep(3.0)               # 3초 유지

except KeyboardInterrupt:   # Ctrl+C 입력 시 무한 루프 종료
    pass

carLedRed.value    = 0
carLedYellow.value = 0
carLedGreen.value  = 0
humanLedRed.value  = 0
humanLedGreen.value= 0
