# audio_to_txt

## 음성파일을 텍스트로 변환해주는 프로젝트 파일

Streamlit 웹 앱 배포 버전(`app.py`)과 콘솔 스크립트 버전(`transcribe.py`)이 함께 포함된 GitHub 저장소용 **`README.md`** 파일 내용입니다. 프로젝트 루트 폴더에 `README.md` 이름으로 저장하여 사용하시면 됩니다.

---

````markdown
# 🎙️ Whisper Audio to Text Converter

OpenAI Whisper 모델을 활용하여 오디오 파일(.mp3, .wav 등)을 텍스트로 변환해 주는 프로젝트입니다.
웹 브라우저 기반의 **Streamlit 앱(`app.py`)**과 터미널 기반의 **콘솔 스크립트(`transcribe.py`)**를 모두 제공하여 목적에 맞게 활용할 수 있습니다.

---

## 📂 프로젝트 구조 (Repository Structure)

- **`app.py`**: Streamlit 기반의 웹 UI 애플리케이션 (클라우드 무료 배포용 메인 파일)
- **`transcribe.py`**: 터미널 환경에서 직접 실행하고 모델이나 코드를 커스텀하여 테스트해 볼 수 있는 콘솔용 스크립트
- **`requirements.txt`**: 프로젝트 구동에 필요한 최소한의 핵심 패키지 목록
- **`howto.md`**: ai모델 사용법에 대한 간단한 설명입니다.

---

## 🚀 시작하기 및 로컬 실행 방법 (How to Run)

### 1. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate
```
````

### 2. 필수 라이브러리 설치

```bash
pip install -r requirements.txt

```

---

## 💻 사용 방법

### 옵션 A: 웹 인터페이스로 실행하기 (`app.py`)

Streamlit을 이용해 브라우저 화면에서 오디오를 업로드하고 변환 결과를 확인할 수 있습니다.

```bash
streamlit run app.py

```

- 브라우저가 자동으로 열리며(`http://localhost:8501`), 파일을 드래그 앤 드롭하여 간편하게 변환할 수 있습니다.
- **Streamlit Community Cloud** 등을 통해 무료로 웹에 배포하여 남들과 공유하기에 가장 적합한 형태입니다.

### 옵션 B: 터미널 콘솔 스크립트로 실행하기 (`transcribe.py`)

코드 수정이나 모델 옵션 변경, 혹은 로컬에서 직접 텍스트 추출 작업을 테스트하고 싶을 때 사용합니다.

```bash
python transcribe.py

```

- 실행 후 사용할 모델(`base`, `small`, `medium` 등)과 변환할 오디오 파일명을 직접 입력하여 구동할 수 있습니다.

---

## 🛠️ 커스텀 및 수정 안내 (Customizing)

- 본 저장소에는 웹 배포용 `app.py` 외에도 `transcribe.py`가 함께 포함되어 있습니다.
- 텍스트 추출 로직을 수정하거나, 자막 타임스탬프(`word_timestamps`) 추가, 혹은 출력 포맷을 바꾸는 등의 실험과 변경을 원하신다면 `transcribe.py` 파일을 자유롭게 수정하여 테스트해 보실 수 있습니다.

```

```
