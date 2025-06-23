import subprocess
import os
import sys

def extract_audio(video_path):
    base, ext = os.path.splitext(video_path)
    output_path = f"{base}_audio{ext}"
    command = [
        'ffmpeg',
        '-vn',
        '-i', video_path,
        '-acodec', 'copy',
        output_path
    ]

    print (f"executing command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True, capture_output=False)
        print(f"\nAudio successfully cut to: {output_path}")
        return True
    except FileNotFoundError:
        print("Error: FFmpeg not found. Please ensure FFmpeg is installed and accessible in your system's PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error trimming video: FFmpeg command failed. {e.returncode}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_video_file = sys.argv[1]
    else:
        print("No input video file found.")

    if not os.path.exists(input_video_file):
        print(f"'{input_video_file}' not found.")

    if extract_audio(input_video_file):
        print("\nAudio extraction process completed.")
    else:
        print("\nAudio extraction process failed.")
