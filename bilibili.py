import yt_dlp
import os
from pathlib import Path

def download_bilibili_video(bv_id, output_dir='downloads'):
    """使用 yt-dlp 下载B站视频（自动处理音视频合并）"""
    try:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': str(output_dir / f'%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': False,
            'extractor_args': {
                'bilibili': ['--no-playlist']
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.bilibili.com/video/{bv_id}'])
            
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False