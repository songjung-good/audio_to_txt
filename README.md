# 🎙️ Audio & YouTube Text Converter (Whisper)

OpenAI Whisper 모델을 활용하여 로컬 오디오 파일(.mp3, .wav 등)과 **유튜브(YouTube) 영상 링크**를 타임스탬프가 포함된 텍스트(`.txt`)로 손쉽게 변환해 주는 웹 애플리케이션 및 콘솔 툴입니다.

👉 **[웹 서비스 바로가기 (Live Demo)](https://audio-to-txt.streamlit.app/)**

---

## Table of Contents

- [Features](#features)
- [Quick Start (Local Deployment)](#quick-start-local-deployment)
- [Repository Structure](#repository-structure)
- [User Guides](#user-guides)
- [Developer & Customization Guides](#developer--customization-guides)
- [FAQ](#faq)

---

## Features

- **다양한 소스 지원**: 로컬 오디오 파일 업로드(`mp3`, `wav`, `m4a`, `ogg`) 및 유튜브 URL 자동 다운로드 변환 지원
- **타임스탬프 자동 기록**: 변환된 텍스트 결과에 문장별 시작/종료 시간(`[MM:SS --> MM:SS]`) 기본 포함
- **모델 동적 선택**: 사양과 속도에 맞춰 `base`, `small`, `medium` 모델 선택 가능
- **실시간 파일 다운로드**: 변환 완료 즉시 화면 프리뷰 확인 및 결과 텍스트 파일(.txt) 원클릭 다운로드 제공
- **웹/콘솔 듀얼 지원**: Streamlit 클라우드 웹 배포 버전과 로컬 테스트용 콘솔 스크립트 동시 제공

---

## Quick Start (Local Deployment)

로컬 환경에서 직접 실행하거나 코드를 수정하여 테스트하고 싶다면 아래 단계를 따르세요.

### 1. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate

```

### 2. 필수 라이브러리 설치

```bash
pip install -r requirements.txt

```

### 3. 애플리케이션 실행

```bash
streamlit run app.py

```

- 브라우저가 자동으로 실행되며 `http://localhost:8501`에서 앱을 직접 테스트할 수 있습니다.

---

## Repository Structure

- **`app.py`**: Streamlit 기반의 웹 UI 애플리케이션 (유튜브 다운로드, 타임스탬프 파싱, 파일 업로드 기능 포함 메인 파일)
- **`transcribe.py`**: 터미널 환경에서 직접 실행하고 모델이나 코드를 커스텀하여 테스트해 볼 수 있는 콘솔용 스크립트
- **`requirements.txt`**: 프로젝트 구동에 필요한 최소한의 핵심 패키지 목록 (`openai-whisper`, `streamlit`, `yt-dlp` 등)
- **`howto.md`**: AI 모델 사용법 및 세부 옵션에 대한 간단한 가이드 설명 파일

---

## User Guides

### 1. 웹 인터페이스로 사용하기 (`app.py` / 라이브 서비스)

1. [오디오 & 유튜브 텍스트 변환기 웹 링크](https://audio-to-txt.streamlit.app/)에 접속합니다.
2. 상단 셀렉트박스에서 사용할 **Whisper 모델 크기**를 선택합니다. (클라우드 환경에서는 `base` 또는 `small` 권장)
3. **[오디오 파일 업로드]** 탭 또는 **[유튜브 URL 입력]** 탭 중 원하는 방식을 선택합니다.
4. 파일을 올리거나 유튜브 주소를 넣은 뒤 **[텍스트 변환 시작]** 버튼을 클릭합니다.
5. 화면에 출력된 타임스탬프 결과 확인 후 **[결과 텍스트 파일(.txt) 다운로드]** 버튼을 눌러 저장합니다.

### 2. 터미널 콘솔 스크립트로 실행하기 (`transcribe.py`)

로컬 환경에서 텍스트 추출 작업을 독립적으로 테스트하거나 자동화하고 싶을 때 사용합니다.

```bash
python transcribe.py

```

- 실행 후 안내에 따라 사용할 모델(`base`, `small`, `medium` 등)과 변환할 오디오 파일명을 직접 입력하여 구동할 수 있습니다.

---

## Developer & Customization Guides

본 프로젝트의 리포지토리에는 웹 배포용 `app.py`뿐만 아니라 콘솔용 `transcribe.py`가 함께 포함되어 있어 소스 코드 레벨에서의 커스텀이 매우 용이합니다.

- 텍스트 추출 로직을 수정하거나, 자막 타임스탬프 포맷을 변경하고 싶다면 `transcribe.py` 또는 `app.py` 파일을 자유롭게 수정하여 실험해 볼 수 있습니다.
- 모델 활용법에 대한 상세한 내용은 리포지토리 내의 **`howto.md`** 문서를 참고해 주세요.

---

## FAQ

### Q. Streamlit 클라우드 배포 시 무거운 모델(medium 이상)을 써도 되나요?

**A:** Streamlit Community Cloud의 무료 티어는 메모리(RAM)와 CPU 자원이 한정되어 있습니다. `medium` 이상의 무거운 모델을 사용할 경우 메모리 부족(OOM)으로 앱이 멈출 수 있으므로, 클라우드 환경에서는 **`base` 또는 `small` 모델** 사용을 권장합니다.

### Q. 유튜브 영상 다운로드가 정상 작동하지 않아요.

**A:** 유튜브 플랫폼의 정책 변경에 따라 `yt-dlp` 라이브러리의 버전 최신화가 필요할 수 있습니다. 로컬 환경인 경우 `pip install --upgrade yt-dlp` 명령어로 업그레이드 후 다시 시도해 주세요.

```

```
