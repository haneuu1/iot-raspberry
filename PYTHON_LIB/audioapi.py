# 음성 인식/합성을 위한 helper 함수 제작

# 음성 합성 함수명 tts()
#     매개변수: 합성할 문자열, 음색(디폴트값 지정)
#     반환값: 성공여부, mp3 데이터

# 음성 인식 함수명 stt()
#     매개변수 : 음성 데이터
#     변환값 : 성공여부, 인식 문자열

import requests
import json
import io

API_KEY = "d05c81a18ee102edcf186c513795470a"

TTS_URL = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
TTS_HEADERS = {
    "Content-Type" : "application/xml",
    "Authorization" : "KakaoAK d05c81a18ee102edcf186c513795470a"
}

SST_URL = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
SST_HEADERS = {
    "Content-Type": "application/octet-stream",
    "X-DSS-Service": "DICTATION",
    "Authorization": "KakaoAK " + API_KEY
}

# 음성 합성
def tts(input_str, voice="WOMAN_READ_CALM"):
    xml = f'<speak><voice name="{voice}">{input_str}</voice></speak>'
    res = requests.post(TTS_URL, headers = TTS_HEADERS, data=xml.encode('utf-8'))
    
    if res.status_code == 200:# 성공
        return True, res.content
    else:   # 실패
        return False, res.json()

# 음성 인식
def stt(audio):
    res = requests.post(SST_URL, headers=SST_HEADERS, data=audio)
    if res.status_code == 200:
        success = True
        sx = res.text.find('{"type":"finalResult"')
        ex = res.text.rindex('}') + 1
        if sx == -1: # 인식에 실패한 경우
            success = False
            sx = res.text.find('{"type":"errorCalled"')
        
        result_json_string = res.text[sx:ex]
        result = json.loads(result_json_string)
        return success, result['value']
    else:
        return False, res.json()