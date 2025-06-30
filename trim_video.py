import subprocess
import os
import sys

def trim_video(video_path, start_time, end_time):
    base, ext = os.path.splitext(video_path)
    output_path = f"{base}_trimmed{ext}"
    if end_time == '':
        command = [
            'ffmpeg',
            '-y',
            '-ss', start_time,
            '-i', video_path,
            '-c', 'copy',
            output_path
        ]
    else:
        command = [
            'ffmpeg',
            '-y',
            '-ss', start_time,
            '-to', end_time,
            '-i', video_path,
            '-c', 'copy',
            output_path
        ]

    print (f"executing command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True, capture_output=False)
        print(f"\nVideo successfully trimmed to: {output_path}")
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



    if trim_video(input_video_file, input("Start time (s): "), input("End time (s): ")):
        print("\nVideo trim process completed.")
    else:
        print("\nVideo trim process failed.")
