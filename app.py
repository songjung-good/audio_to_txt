import os
import streamlit as st
import whisper

# 페이지 설정
st.set_page_config(page_title="Whisper 음성 텍스트 변환기", page_icon="🎙️", layout="centered")

st.title("🎙️ AI 음성 텍스트 변환기 (Whisper)")
st.write("오디오 파일(.mp3, .wav 등)을 업로드하면 OpenAI Whisper가 텍스트로 변환해 줍니다.")

# 1. 모델 선택 옵션 (사이드바 또는 메인 화면)
model_size = st.selectbox(
    "사용할 Whisper 모델 선택 (클라우드 환경에서는 small 또는 base 권장)",
    ("base", "small", "medium"),
    index=1
)

# 모델 로드 (캐싱을 적용하여 최초 한 번만 로드되도록 최적화)
@st.cache_resource
def load_whisper_model(size):
    return whisper.load_model(size)

with st.spinner(f"[{model_size}] 모델을 불러오는 중입니다... 잠시만 기다려주세요."):
    model = load_whisper_model(model_size)

# 2. 오디오 파일 업로드 컴포넌트
uploaded_file = st.file_uploader("변환할 오디오 파일을 업로드하세요", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    # 업로드된 파일을 임시로 저장
    input_path = uploaded_file.name
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(uploaded_file, format='audio/mp3')
    
    if st.button("🚀 텍스트 변환 시작"):
        try:
            with st.spinner("음성을 텍스트로 변환하는 중입니다... (오디오 길이에 따라 시간이 걸릴 수 있습니다)"):
                # Whisper 변환 실행
                result = model.transcribe(input_path, language="Korean")
                transcribed_text = result["text"]
            
            st.success("변환이 완료되었습니다!")
            
            # 결과 화면 출력
            st.text_area("변환된 텍스트 결과", transcribed_text, height=250)
            
            # 텍스트 파일 다운로드 버튼 제공
            base_name, _ = os.path.splitext(input_path)
            output_txt = f"{base_name}_result.txt"
            
            st.download_button(
                label="📥 결과 텍스트 파일(.txt) 다운로드",
                data=transcribed_text,
                file_name=output_txt,
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"변환 중 오류가 발생했습니다: {e}")
            
        finally:
            # 임시 파일 정리
            if os.path.exists(input_path):
                os.remove(input_path)