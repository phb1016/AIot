import urllib.request # 웹에서 데이터를 가져오기 위한 라이브러리
import json # JSON 데이터를 다루기 위해 사용
import datetime # 시간 계산을 위한 라이브러리
import asyncio # 비동기 루프를 돌리기 위해 필요
from telegram import Bot # 텔레그램 봇 기능을 쓰기 위해 임포트

telegram_id = '8693571041' # 내 텔레그램 ID 숫자
my_token = '8406415581:AAHX54FYYt6LxjhJbhlP1aEw2ZDxW0yf6ZA' # 봇 토큰 값
api_key = 'Enter your API key here' # 발급받은 날씨 API 키
bot = Bot(token=my_token) # 봇 객체 생성

ALERT_HOURS = [7, 10, 13, 16, 19, 22] # 정각 알림 시간대 설정
ALERT_TIMES = ["08:30", "14:45"] # 따로 정해둔 특정 알림 시간

def getWeather(): # 날씨 정보를 가져오는 함수 시작
    # 날씨 예보 API 호출 URL
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"
    with urllib.request.urlopen(url) as r: # URL로 데이터 요청
        data = json.loads(r.read()) # 받은 데이터를 JSON으로 로드
        text = "" # 메시지 담을 변수
        for i in range(8): # 3시간 단위로 8번 반복해서 데이터 추출
            item = data['list'][i]
            # 시간 값을 가져와서 한국 시간 기준(+9)으로 계산
            hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
            temp = item['main']['temp'] # 기온 데이터
            humi = item['main']['humidity'] # 습도 데이터
            desc = item['weather'][0]['description'] # 날씨 상태 정보
            # 한 줄씩 텍스트로 정리
            text += f"({hour}h {temp}C {humi}% {desc})\n"
        return text # 최종 날씨 메시지 반환

async def main(): # 메인 비동기 함수 시작
    try:
        while True: # 무한 루프 가동
            now = datetime.datetime.now() # 지금 시각 확인
            hm = now.strftime('%H:%M') # 시:분 형태로 저장
            # 정각 알림 조건이랑 지정 시간 알림 조건 확인
            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0
            is_alert_time = hm in ALERT_TIMES and now.second == 0
            
            if is_alert_hour or is_alert_time: # 둘 중 하나라도 조건이 맞으면 실행
                msg = getWeather() # 날씨 데이터 가져오기
                print(msg) # 터미널에 먼저 출력해보기
                await bot.send_message(chat_id=telegram_id, text=msg) # 텔레그램으로 전송
                
            await asyncio.sleep(1) # 1초 대기 후 다시 시각 체크
    except KeyboardInterrupt: # 강제 종료 시 예외 처리
        pass

asyncio.run(main()) # 프로그램 실행
