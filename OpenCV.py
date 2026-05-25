import cv2 # OpenCV 라이브러리불러오기
from gpiozero import Buzzer # GPIO 부저제어클래스불러오기
import time # 시간관련라이브러리불러오기
buzzerPin = Buzzer(16) # GPIO 16번핀에부저객체생성
def main():
    camera = cv2.VideoCapture(-1) # 웹캠자동탐지후열기
    camera.set(3, 640) # 가로해상도640픽셀설정
    camera.set(4, 480) # 세로해상도480픽셀설정
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml' # 얼굴탐지모델경로
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml' # 눈탐지모델경로
    face_cascade = cv2.CascadeClassifier(face_xml) # 얼굴탐지분류기생성
    eye_cascade = cv2.CascadeClassifier(eye_xml) # 눈탐지분류기생성
    while( camera.isOpened() ): # 카메라열려있는동안반복
        _, image = camera.read() # 프레임한장캡처
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # 흑백이미지로변환
        faces = face_cascade.detectMultiScale(gray, # 흑백이미지에서얼굴탐지
                                              scaleFactor=1.1, # 탐지윈도우10%씩확대
                                              minNeighbors=5, # 최소5회탐지시얼굴확정
                                              minSize=(100,100), # 탐지최소크기100×100
                                              flags=cv2.CASCADE_SCALE_IMAGE) # 이미지스케일링방식탐지
        print("faces detected Number: " + str(len(faces))) # 탐지된얼굴수터미널출력
        if len(faces): # 얼굴이1개이상이면
            for (x, y, w, h) in faces: # 얼굴좌표순회
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2) # 얼굴에파란사각형그리기
                face_gray = gray[y:y+h, x:x+w] # 얼굴영역흑백이미지추출
                face_color = image[y:y+h, x:x+w] # 얼굴영역컬러이미지추출
                eyes = eye_cascade.detectMultiScale(face_gray, # 얼굴영역에서눈탐지
                                                    scaleFactor=1.1, # 탐지윈도우10%씩확대
                                                    minNeighbors=5) # 최소5회탐지시눈확정
                if len(eyes) <= 1: buzzerPin.on() # 눈1개이하→ 부저켜기
                else: buzzerPin.off() # 눈2개이상→ 부저끄기
                for (ex,ey,ew,eh) in eyes: # 눈좌표순회
                    cv2.rectangle(face_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2) # 눈에초록사각형그리기
        cv2.imshow('result', image) # 결과이미지GUI 창출력
        if cv2.waitKey(1) == ord('q'): break # q 키입력시종료
    cv2.destroyAllWindows() # 모든OpenCV 창닫기
    buzzerPin.off() # 부저강제끄기
if __name__ == '__main__': main() # 직접실행시main() 호출
