import speech_recognition as sr  # 음성 인식 처리를 위한 모듈 로드
import requests                 # 날씨 API 호출을 위한 HTTP 통신 모듈 로드
import os                       # 시스템 명령어(espeak) 실행을 위한 모듈 로드
import time                     # 시간 지연 제어를 위한 모듈 로드

API_KEY = ""  # OpenWeatherMap에서 발급받은 인증키
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"  # 서울 날씨 데이터 요청 주소 (섭씨 기준)

def speak(option, msg):
    """지정된 옵션으로 텍스트를 음성 변환하여 출력하는 함수"""
    os.system("espeak {} '{}'".format(option, msg))  # espeak 프로그램을 사용해 메시지 낭독

try:
    while True:  # 사용자가 강제 종료할 때까지 무한 반복 실행
        r = sr.Recognizer()  # 음성 인식 컨트롤러 객체 생성
        
        with sr.Microphone() as source:  # 시스템 기본 마이크를 입력 장치로 지정
            print("Say something!")     # 사용자 음성 입력 대기 안내문 출력
            audio = r.listen(source)    # 마이크로부터 들어오는 오디오 데이터 캡처

        try:
            # 구글 음성 인식 엔진을 이용해 오디오를 한국어 텍스트로 변환
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)   # 인식된 결과 텍스트 화면에 표시
            
            if text in "날씨":           # 인식된 단어에 '날씨'라는 키워드가 포함되어 있는지 확인
                print("날씨 음성을 인식하였습니다.")
                
                response = requests.get(url)  # 기상 정보 API 서버에 데이터 요청
                data = response.json()         # 수신된 응답 데이터를 JSON 구조로 분석
                
                temp = data["main"]["temp"]       # 기온 데이터 추출
                humi = data["main"]["humidity"]   # 습도 데이터 추출
                
                # 음성으로 출력할 안내 메시지 구성 (기온은 정수로 변환)
                msg = ' 기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                # espeak 전용 설정 (말하기 속도 180, 톤 50, 볼륨 200, 한국어 여성 목소리)
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                
                speak(option, msg)  # 생성된 메시지를 음성으로 출력
                
        except sr.UnknownValueError:
            # 오디오 음량이 너무 작거나 단어 판별이 불가능한 경우 예외 처리
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            # 구글 서버 네트워크 장애 또는 API 제한 발생 시 예외 처리
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    # 사용자가 Ctrl+C를 눌렀을 때 오류 없이 안전하게 프로그램 종료
    pass
