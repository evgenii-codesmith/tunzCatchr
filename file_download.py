import subprocess

def get_file_from_youtube(url, file_format, audio_quality):
    """
    file_format: String :'best', 'aac','flac','mp3','m4a','opus','vorbis', 'wav'
    audio_quality: String: value from '0'(better) to '9'(worse) or specific bitrate ie '128K'
    See youtube-dl -h for more info.
    """
    proc = subprocess.Popen(
        ["youtube-dl","--extract-audio","--audio-format",file_format, "--audio-quality",audio_quality, url],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,) 
    
    output, errors = proc.communicate()
    print (output.decode('utf-8'), errors)
