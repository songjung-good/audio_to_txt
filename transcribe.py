import os
import sys
import whisper

def format_time(seconds):
    """초 단위를 보기 편한 MM:SS 포맷으로 변환하는 함수"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def main():
    print("=== Whisper 오디오 텍스트 변환기 (타임스탬프 포함) ===")
    
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

    # 2. 변환할 오디오 파일명 입력
    audio_file = input('변환할 오디오 파일명을 입력하세요 (예: AI1-1.mp3): ').strip()

    if not os.path.exists(audio_file):
        print(f"[오류] '{audio_file}' 파일을 찾을 수 없습니다. 파일 경로와 이름을 확인해 주세요.")
        return

    try:
        print(f"\n'{audio_file}' 파일 변환을 시작합니다 (타임스탬프 추출 중)...")
        base_name, _ = os.path.splitext(audio_file)
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