import subprocess
import os
import math
import sys

def get_video_info(video_path):
    if not os.path.exists(video_path):
        print(f"8 Error: Input video file not found at '{video_path}'")
        return None, None, None
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) == 3:
            width = int(lines[0])
            height = int(lines[1])
            duration = float(lines[2])
            return duration, width, height
        else:
            print(f"Error: unexpected ffprobe output: {result.stdout}")
            return None, None, None
    except FileNotFoundError as e:
        print(f"Error: ffprobe not found. Please install ffmpeg :) (and ensure it's in PATH) | {e}")
        return None, None, None
    except subprocess.CalledProcessError as e:
        print(f"Error calling ffprobe: {e}")
        print(f"Stderr: {e.stderr}")
        return None, None, None
    except ValueError:
        print(f"Error: Could not parse duration from ffprobe: {result.stdout}")
        return None, None, None
def get_next_16_9_resolution(current_width,current_height):
    standard_16_9_resolutions = [
        (3840, 2160),  # 4K UHD
        (2560, 1440),  # 1440p
        (1920, 1080),  # 1080p
        (1280, 720),  # 720p
        (854, 480),  # 480p
        (640, 360),  # 360p
        (426, 240)  # 240p
    ]
    target_width, target_height = current_width, current_height
    current_aspect_ratio = current_width / current_height
    if not (16 / 9 - 0.01 <= current_aspect_ratio <= 16 / 9 + 0.01):
        print(f"Warning: Original video aspect ratio ({current_aspect_ratio:.2f}) is not 16:9. "
              "Scaling to a 16:9 target resolution might cause distortion.")
    found_target = False
    for res_w, res_h in standard_16_9_resolutions:
        if current_height > res_h:
            target_width, target_height = res_w, res_h
            found_target = True
            break
    if not found_target and current_height <= standard_16_9_resolutions[-1][1]:
        print("Video resolution is already at or below the smallest standard 16 9 resolution. No resolution scaling applied.")
        return None, None
    print(f"Original resolution is {current_width}x{current_height}. Calculated resolution is {target_width}x{target_height}.")
    return target_width, target_height

def compress_video(input_path, target_size_mb = 10, audio_bitrate_kbps = 96):
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_compressed{ext}"

    print(f"Starting compression for '{input_path}'")
    print(f"Target size is {target_size_mb} MB")
    print(f"Audio bitrate is {audio_bitrate_kbps}kbps")

    video_duration, original_width, original_height = get_video_info(input_path)
    if video_duration is None or original_width is None or original_height is None:
        print("Failed to get video duration")
        return False
    print(f"Video duration: {video_duration:.2f} seconds")

    scale_width, scale_height = get_next_16_9_resolution(original_width, original_height)

    target_size_bits = target_size_mb * 8 * 1024 * 1024

    audio_bitrate_bps = audio_bitrate_kbps * 1000

    total_bitrate_bps = target_size_bits / video_duration

    video_bitrate_bps = max(0, total_bitrate_bps - audio_bitrate_bps)

    video_bitrate_kbps = video_bitrate_bps / 1000

    if video_bitrate_kbps <= 0:
        print("Warning: Calculated video bitrate is too low.")
        print("Continuing with minimum bitrate")
        video_bitrate_kbps = 1000

    print(f"Calculated target video bitrate: {video_bitrate_kbps:.2f}kbps")

    # FFmpeg command construction
    # -i: input file
    # -b:v: video bitrate
    # -b:a: audio bitrate
    # -c:v libx264: use h.264 video codec (common and efficient)
    # -preset veryfast: compression speed vs. quality. 'veryfast' is a good balance.
    #                   Other options: ultrafast, superfast, faster, fast, medium, slow, slower, veryslow
    # -crf 23: Constant Rate Factor (CRF). Lower value means higher quality, larger file size.
    #          Usually 23 is a good default. When using -b:v, CRF might be ignored or used differently.
    #          For target size, -b:v is more direct.
    # -c:a aac: use AAC audio codec (common and efficient)
    # -movflags +faststart: optimizes the file for web streaming
    # -y: overwrite output file without asking
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-b:v', f'{video_bitrate_kbps:.0f}k',
        '-b:a', f'{audio_bitrate_kbps}k',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-c:a', 'aac',
        '-movflags', '+faststart',
        '-y',
        output_path
    ]
    if scale_width is not None and scale_height is not None:
        scaled_w_even = math.floor(scale_width/2) *2
        scaled_h_even = math.floor(scale_height/2) *2
        cmd.extend(['-vf', f'scale={scaled_w_even}:{scaled_h_even}'])
        print (f"Applying resolution scale: {scaled_w_even}x{scaled_h_even}")

    print(f"\nFFmpeg command: {' '.join(cmd)}\n")

    try:
        process = subprocess.run(cmd, capture_output=False, check=True)
        print(f"\nCompression finished. Output saved to '{output_path}'")

        if (os.path.exists(output_path)):
            output_file_size_bytes = os.path.getsize(output_path)
            output_file_size_mb = output_file_size_bytes / 1024 / 1024
            print(f"Actual output file size: {output_file_size_mb:.2f} MB")
            if output_file_size_mb <= target_size_mb:
                print("Success")
                return True
            else:
                print("Failed to compress below target")
                return False
        else:
            print("Failed to create output file")
            return False

    except FileNotFoundError:
        print ("FFmpeg not found. Please install ffmpeg :(")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error calling ffmpeg: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_video_file = sys.argv[1]
        desired_size_mb = 10
    else:
        print("No input video file found.")

    if not os.path.exists(input_video_file):
        print(f"'{input_video_file}' not found.")

    if compress_video(input_video_file, desired_size_mb):
        print("\nVideo Compression process completed.")
    else:
        print("\nVideo compression process failed.")



