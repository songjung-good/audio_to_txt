import os
import streamlit as st
import whisper
from yt_dlp import YoutubeDL

# 페이지 설정
st.set_page_config(
    page_title="유튜브 및 오디오 AI 텍스트 변환기 (Whisper)",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 검색로봇이 읽을 수 있는 메인 키워드 소개글 삽입
st.markdown(
    """
    <meta name="description" content="유튜브 URL 링크나 MP3 오디오 파일을 업로드하면 OpenAI Whisper로 타임스탬프 포함 텍스트(.txt) 변환을 무료로 제공하는 웹 서비스입니다.">
    <meta name="google-site-verification" content="google7aa728652332ce67">
    """,
    unsafe_allow_html=True,
)

st.title("🎙️ AI 음성 & 유튜브 텍스트 변환기 (타임스탬프 포함)")
st.write("오디오 파일을 업로드하거나 유튜브 URL을 입력하면 타임스탬프가 포함된 텍스트로 변환해 줍니다!")

# 1. 모델 선택 옵션
model_size = st.selectbox(
    "사용할 Whisper 모델 선택 (클라우드 환경에서는 base 또는 small 권장)",
    ("base", "small", "medium"),
    index=1
)

# 모델 로드 최적화 (캐싱 적용)
@st.cache_resource
def load_whisper_model(size):
    return whisper.load_model(size)

with st.spinner(f"[{model_size}] 모델을 불러오는 중입니다... 잠시만 기다려주세요."):
    model = load_whisper_model(model_size)

# 2. 입력 방식 탭 나누기 (파일 업로드 vs 유튜브 URL)
tab1, tab2 = st.tabs(["📁 오디오 파일 업로드", "🔗 유튜브 URL 입력"])

input_path = None
original_title = "audio"

with tab1:
    uploaded_file = st.file_uploader("변환할 오디오 파일을 업로드하세요", type=["mp3", "wav", "m4a", "ogg"])
    if uploaded_file is not None:
        original_title, _ = os.path.splitext(uploaded_file.name)
        input_path = f"{original_title}.mp3"
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.audio(uploaded_file, format='audio/mp3')

with tab2:
    youtube_url = st.text_input("유튜브 영상 URL을 입력하세요", placeholder="https://www.youtube.com/watch?v=...")
    if youtube_url:
        if st.button("📥 유튜브 오디오 다운로드"):
            try:
                with st.spinner("유튜브에서 오디오를 추출하는 중입니다..."):
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'youtube_audio.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                    with YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(youtube_url, download=True)
                        original_title = info_dict.get('title', 'youtube_video').replace('/', '_')
                    
                    input_path = "youtube_audio.mp3"
                    st.success("유튜브 오디오 다운로드 완료!")
                    st.audio(input_path, format='audio/mp3')
            except Exception as e:
                st.error(f"유튜브 오디오 다운로드 중 오류 발생: {e}")

# 시간을 보기 좋은 포맷(MM:SS)으로 바꿔주는 함수
def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

# 3. 변환 실행 버튼
if input_path and os.path.exists(input_path):
    if st.button("🚀 텍스트 변환 시작 (타임스탬프 포함)"):
        try:
            with st.spinner("음성을 텍스트로 변환하는 중입니다... (영상의 길이에 따라 시간이 걸릴 수 있습니다)"):
                # Whisper 변환 실행
                result = model.transcribe(input_path, language="Korean")
                
                # 세그먼트별로 타임스탬프와 텍스트 조합
                formatted_lines = []
                plain_text_for_download = []
                
                for segment in result["segments"]:
                    start_time = format_time(segment["start"])
                    end_time = format_time(segment["end"])
                    text = segment["text"].strip()
                    
                    line = f"[{start_time} --> {end_time}] {text}"
                    formatted_lines.append(line)
                    plain_text_for_download.append(line)
                
                final_output_text = "\n".join(plain_text_for_download)
            
            st.success("변환이 완료되었습니다!")
            
            # 결과 화면 출력 (스크롤 가능한 텍스트 영역)
            st.text_area("타임스탬프가 포함된 결과", final_output_text, height=300)
            
            # 텍스트 파일 다운로드 버튼 제공
            output_txt = f"{original_title}_timestamp_result.txt"
            st.download_button(
                label="📥 결과 텍스트 파일(.txt) 다운로드",
                data=final_output_text,
                file_name=output_txt,
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"변환 중 오류가 발생했습니다: {e}")
            
        finally:
            # 임시 오디오 파일 정리
            if os.path.exists(input_path) and input_path != "youtube_audio.mp3":
                os.remove(input_path)