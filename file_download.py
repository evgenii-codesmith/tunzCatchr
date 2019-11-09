import subprocess


def get_file_from_youtube(db, target_tune, file_format, audio_quality):
    """
    file_format: String :'best', 'aac','flac','mp3','m4a','opus','vorbis',
    'wav'
    audio_quality: String: value from '0'(better) to '9'(worse)
    or specific bitrate ie '128K'
    See youtube-dl -h for more info.
    """
    output_template = "./Downloaded/%(title)s.%(ext)s"
    proc = subprocess.Popen(
        ["youtube-dl", "--extract-audio", "--audio-format", file_format,
         "--audio-quality", audio_quality, "-o", output_template,
         target_tune.url, ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

    output, error = proc.communicate()

    if error:
        print(error)
        return None

    target_tune.downloaded = True

    try:
        db.session.commit()
    except Exception as e:
        print(e)
