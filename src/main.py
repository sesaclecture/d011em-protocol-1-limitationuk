#!/usr/bin/env python3
# pylint: disable=import-error

"""
GPIO 과제
- gpiozero 라이브러리 사용

UART 과제
- pyserial 라이브러리 사용
- UART 통신: 115200 bps, 8N1, 플로우 제어 없음
- TXD3/RXD3을 활용
"""

import sys
import time

from gpiozero import LED, Button
from serial import Serial


def blink_led() -> None:
    """
    [문제 1] 18번 핀에 연결된 LED를 1초 간격으로 ON/OFF를 10번 반복
    - gpiozero.LED 사용
    - 종료시 LED는 OFF 상태
    """
    # TODO: blink_led 구현
    led = LED(18)

    for _ in range(10):
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
      

def check_to_input_button() -> None:
    """
    [문제 2] 18번 핀 버튼 입력을 받아서
      - 눌렸을 때: 'pressed'
      - 뗐을 때:   'released'
    를 출력한다.
    - polling 방식으로 구현할 것.
    - 버튼 입력을 10번 받았으면 종료.
    """
    # TODO: check_to_input_button 구현

    btn = Button(18, pull_up=True)
    prev = btn.is_pressed
    count = 0

    while True:
        # 현재 눌림 상태 읽기(True=눌림, False=떼어짐)
        cur = btn.is_pressed

        if count >= 10: #10번 받았으면 종료
            break

        # 상태 변화가 있을 때만 출력
        if cur != prev:
            if cur:
                print("pressed")    # 눌리면 출력
                count += 1
            else:
                print("released")   # 떼어지면 출력
            prev = cur  # 이전 상태 갱신
        
        # 짧게 대기하여 cpu 과부하 방지
        time.sleep(0.01)
    


def blink_led_through_button() -> None:
    """
    [문제 3]
    - 12번: LED 출력
    - 13번: Button 입력
    - 버튼이 눌려 있는 동안에만 LED가 0.5초 간격으로 깜빡인다.
    - 버튼이 10번 눌려졌으면 종료.
    - 종료시 LED는 OFF 상태
    """
    # TODO: blink_led_through_button 구현
    led = LED(12)
    btn = Button(13, pull_up=True)
    count = 0
    
   
    if btn.is_pressed:
        count += 1
        if count >= 10:
            return
        else:
            while btn.is_pressed:
                led.on()
                time.sleep(0.5)
                led.off()
                time.sleep(0.5)

def transmit_msg() -> None:
    """
    [문제 1] UART3로 "Hello World! {i}" 문자열을 1초마다 전송
    - 총 10번 전송 후 종료
    - 개행을 붙여 전송 (수신/테스트 편의)
    """
    # TODO: blink_led_through_button 구현

    ser = Serial("/dev/ttyAMA3", baudrate=115200, timeout=1.0)
    
    for i in range(10):
        msg = f"Hello World! {i}\n"
        ser.write(msg.encode())
        time.sleep(1)

    ser.close()


def receive_msg() -> None:
    """
    [문제 2] UART료3에서 줄 단위로 읽어 화면에 출력.
    - 'exit' (대소문자 무시) 라인을 수신하면 함수 종료
    """
    # TODO: receive_msg 구현
    
    # 시리얼 주소
    ser = Serial("/dev/ttyAMA3", baudrate=115200, timeout=1.0)
    buffer = "" # 문자를 임시 저장할 변수

    while True:
        raw = ser.read().decode() # 시리얼에서 한 글자 읽기(디코딩)
        if not raw: # 데이터 유무 확인 
            continue  
        buffer += raw   # 버퍼에 입력

        while '\n' in buffer:  # 줄 단위로 처리
                line, buffer = buffer.split('\n', 1) # 첫 번째 줄과 나머지 버퍼로 분리
                print(line)
                if line.lower() == "exit": # exit 수신하면 종료
                    return




if __name__ == "__main__":
    blink_led()
    check_to_input_button()
    blink_led_through_button()

    transmit_msg()
    receive_msg()
