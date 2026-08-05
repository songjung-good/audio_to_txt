## 기본 사용법

````
whisper {audio.mp3} --language Korean --model {medium}
``` 

## 주요 옵션 설명
--model
사용 모델 크기 (tiny, base, small, medium, large)

--language
입력 음성의 언어 지정

--task translate
번역도 동시에 수행 (예: 한국어 → 영어)

--output_format
출력 형식 지정 (txt, srt, vtt 등)


## Whisper 실전 활용 예제
1. 유튜브 영상 자막 추출
youtube-dl -x --audio-format mp3 [유튜브 링크]
whisper video.mp3 --model medium --output_format srt
→ 영상 자막용 .srt 파일 생성
 
2. 회의 음성 녹음 텍스트 변환
whisper meeting_recording.wav --language Korean --model large
→ 텍스트와 타임스탬프 포함된 자막 생성
 
3. 팟캐스트 영어로 번역 & 자막 제작
whisper podcast.mp3 --task translate --model large
→ 한국어 음성을 영어로 번역한 자막 출력
 
### Whisper를 SaaS에 API처럼 활용하고 싶다면?
Whisper는 로컬에서 CLI로 사용할 수도 있지만, Python 코드로 직접 통합하여 웹 서비스에도 연동할 수 있습니다.
 
간단한 Python 예제
```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("your_audio_file.mp3")
print(result["text"])
```
→ 이 코드를 기반으로 Flask나 FastAPI로 API 서버를 만들 수 있습니다.

### 마무리 팁: 모델 선택 기준

tiny / 39MB / 매우 빠름 / 낮음
base / 74MB / 빠름 / 보통
small / 244MB / 중간 / 우수
medium / 769MB / 느림 / 매우 우수
large / 1550MB / 느림 / 최고 정확도

개발 테스트용: tiny, base
실서비스용: small, medium
고정밀 번역용: large
````
