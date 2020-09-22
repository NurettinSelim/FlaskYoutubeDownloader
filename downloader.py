from youtube_dl import YoutubeDL

mp3_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
    }],
}

def download_mp3(url, path):
    mp3_opts['outtmpl'] = path

    with YoutubeDL(mp3_opts) as ydl:
        result = ydl.extract_info(url)
    return result
