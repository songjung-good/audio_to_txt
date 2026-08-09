import os
import re
import shutil
import sys
import whisper

def format_time(seconds):
    """초 단위를 보기 편한 MM:SS 포맷으로 변환하는 함수"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def setup_ffmpeg():
    """ffmpeg 경로를 탐색하고 환경 변수에 자동 등록"""
    # 1. 시스템 PATH에 이미 ffmpeg가 있는지 확인
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    # 2. macOS 일반 경로 확인 (/opt/homebrew/bin, /usr/local/bin)
    for path in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"]:
        if os.path.exists(path):
            ffmpeg_dir = os.path.dirname(path)
            if ffmpeg_dir not in os.environ.get("PATH", ""):
                os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
            return path

    # 3. imageio_ffmpeg 패키지 확인
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        if ffmpeg_exe and os.path.exists(ffmpeg_exe):
            ffmpeg_dir = os.path.dirname(ffmpeg_exe)
            link_path = os.path.join(ffmpeg_dir, "ffmpeg")
            if not os.path.exists(link_path):
                try:
                    os.symlink(ffmpeg_exe, link_path)
                except Exception:
                    pass
            if ffmpeg_dir not in os.environ.get("PATH", ""):
                os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
            return ffmpeg_exe
    except Exception:
        pass

    return None

def is_youtube_or_url(text: str) -> bool:
    """입력값이 유튜브 URL 또는 일반 웹 URL인지 확인하는 함수"""
    text_lower = text.lower()
    return (
        text_lower.startswith(("http://", "https://"))
        or "youtube.com" in text_lower
        or "youtu.be" in text_lower
    )

def normalize_url(url: str) -> str:
    """프로토콜이 빠진 유튜브 URL에 https:// 를 붙여주는 함수"""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url

def sanitize_filename(name: str) -> str:
    """파일명으로 사용할 수 없는 특수문자 제거 및 정제"""
    clean_name = re.sub(r'[\\/*?:"<>|]', "", name)
    clean_name = re.sub(r'\s+', " ", clean_name).strip()
    return clean_name if clean_name else "youtube_audio"

def download_youtube_audio(youtube_url: str):
    """yt_dlp를 사용하여 유튜브 영상에서 오디오(mp3)를 추출하는 함수"""
    ffmpeg_path = setup_ffmpeg()

    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        print("\n[오류] yt_dlp 라이브러리가 설치되어 있지 않습니다.")
        print("터미널에서 'pip install yt-dlp'를 실행하여 설치해 주세요.")
        return None, None

    normalized_url = normalize_url(youtube_url)
    print(f"\n[유튜브 다운로드] 정보를 가져오고 오디오를 추출하는 중입니다: {normalized_url}")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s_%(title).50s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True,
    }

    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(normalized_url, download=True)
            raw_title = info.get('title', 'youtube_audio')
            safe_title = sanitize_filename(raw_title)
            
            # 다운로드된 mp3 파일명 파악
            temp_filename = ydl.prepare_filename(info)
            base_temp, _ = os.path.splitext(temp_filename)
            downloaded_mp3 = f"{base_temp}.mp3"
            
            if not os.path.exists(downloaded_mp3):
                video_id = info.get('id', '')
                for f in os.listdir('.'):
                    if f.startswith(video_id) and f.endswith('.mp3'):
                        downloaded_mp3 = f
                        break
            
            print(f"[다운로드 완료] 영상 제목: '{raw_title}'")
            return downloaded_mp3, safe_title
    except Exception as e:
        print(f"\n[유튜브 다운로드 실패] 오류가 발생했습니다: {e}")
        if "ffmpeg" in str(e).lower() or not ffmpeg_path:
            print("\n💡 [해결 방법 안내]")
            print("1. 파이썬 패키지 설치: pip install -r requirements.txt (또는 pip install imageio-ffmpeg)")
            print("2. 또는 Mac 터미널에서 시스템 ffmpeg 설치: brew install ffmpeg\n")
        return None, None

def main():
    print("=== Whisper 오디오 & 유튜브 텍스트 변환기 (타임스탬프 포함) ===")
    
    # 1. 모델 선택 (기본값 medium 설정)
    model_name = input("사용할 모델을 입력하세요 (tiny, base, small, medium, large 중 선택, 기본값 medium): ").strip()
    if not model_name:
        model_name = "medium"

    try:
        print(f"\n[{model_name}] 모델을 불러오는 중입니다 (최초 실행 시 다운로드가 진행될 수 있습니다)...")
        model = whisper.load_model(model_name)
        print(f"[{model_name}] 모델 로드 완료!\n")
    except Exception as e:
        print(f"[오류] 모델을 로드하는 중 문제가 발생했습니다: {e}")
        return

    # 2. 변환할 대상 입력 (로컬 오디오 파일 또는 유튜브 링크)
    target_input = input("변환할 오디오 파일명 또는 유튜브 링크(URL)를 입력하세요:\n(예: sample.mp3 또는 https://www.youtube.com/watch?v=...): ").strip().strip("'\"")

    if not target_input:
        print("[오류] 입력값이 비어 있습니다.")
        return

    audio_file = None
    base_name = None

    if is_youtube_or_url(target_input):
        audio_file, base_name = download_youtube_audio(target_input)
        if not audio_file or not os.path.exists(audio_file):
            print("[오류] 유튜브 오디오 다운로드에 실패하여 변환을 중단합니다.")
            return
    else:
        audio_file = target_input
        if not os.path.exists(audio_file):
            print(f"[오류] '{audio_file}' 파일을 찾을 수 없습니다. 파일 경로와 이름을 확인해 주세요.")
            return
        base_name, _ = os.path.splitext(os.path.basename(audio_file))

    try:
        print(f"\n'{audio_file}' 음성 변환을 시작합니다 (타임스탬프 추출 중)...")
        output_txt = f"{base_name}_timestamp_result.txt"
        
        # Whisper 변환 실행 (한국어 설정)
        result = model.transcribe(audio_file, language='Korean')

        # 세그먼트별 타임스탬프와 텍스트 조합
        formatted_lines = []
        for segment in result["segments"]:
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])
            text = segment["text"].strip()
            
            line = f"[{start_time} --> {end_time}] {text}"
            formatted_lines.append(line)

        final_output_text = "\n".join(formatted_lines)

        # 결과 저장
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(final_output_text)

        print(f'\n[성공] 변환 완료! 타임스탬프가 포함된 결과가 [{output_txt}] 파일로 저장되었습니다.')

    except Exception as e:
        print(f"\n[변환 실패 오류] 변환 중 예외가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
    input("\n작업이 끝났습니다. 종료하려면 Enter 키를 누르세요.")