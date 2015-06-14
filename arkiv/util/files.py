import mimetypes
import os
from arkiv.match import match_archive

movies = ['avi', 'mpg', 'mpeg', 'mp4', 'm4v', 'mov', 'mkv', 'flv', 'wmv', 'rmvb', '3gp', 'f4v', 'ogm', 'divx', 'asf']

subtitles = ['srt', 'idx', 'sub']

images = ['jpg', 'jpeg', 'bmp', 'gif', 'png', 'tiff']

audio = ['mp3', 'wav', 'flac', 'aac', 'aiff', 'au', 'bwf', 'cdda', 'raw', 'la', 'pac', 'm4a', 'ape', 'wv', 'wma', 'ast',
         'am3', 'mp2', 'mp3', 'mpc', 'ra', 'rm', 'swa', 'vox', 'aup', 'band', 'mid', 'rmj']
documents = ['pdf', 'epub', 'mobi', 'djvu', 'chm', 'cbr', 'cbz']
html = ['html', 'htm', 'aspx', 'asp', 'php', 'jsp', 'shtm']
junk = ['nfo', 'info', 'txt', 'text', 'tex', 'url', 'link', 'idz', 'sfv', 'db', 'dat', 'doc', 'rtf', 'crc']
info = junk + html
applications = ['dmg', 'exe', 'iso', 'apk', 'cab', 'deb', 'rpm', 'nrg', 'ipa', 'app']

archives = ['rar', 'zip', 'bzip2', 'bzip', 'bz2', 'tar', 'gz', 'tgz', '7z', 'jar', 'ace', 'alz', 'at3', 'arc', 'arj',
            'ipg', 'lzip', 'lzo', 'lzma', 'lzx', 'mbw', 'par2', 'par', 'sen', 'sitx', 'sit', 'zoo', 'war', 'xpi']

code = ['json', 'xml', 'py', 'java', 'js', 'c', 'cpp', 'rb', 'sh']

known = movies + subtitles + images + audio + applications
files = known + info + documents + archives + code
useful = archives + movies + images + audio + documents + html + applications
ignore = ['com']


def is_image(item):
    return _extension(item) in images


def is_image_extension(extension):
    return extension and extension.lower() in images


def is_jpg(extension):
    return extension.lower() in ['jpg', 'jpeg']


def is_audio(item):
    return _extension(item) in audio


def _extension(item):
    return item.extension and item.extension.lower()


def is_video(item):
    return _extension(item) in movies


def is_application(item):
    return _extension(item) in applications


def _is_known_mime(file_name):
    return bool(_mime_type(file_name))


def _mime_type(file_name):
    mime, encoding = mimetypes.guess_type(file_name)
    return mime


def filter_extension(file_list, extension_list):
    return filter(lambda f: _extension(f) in extension_list, file_list)


def is_known_file_type(file_name):
    return file_name and (_is_known_type(file_name) or bool(match_archive(file_name)))


def _is_known_type(file_name):
    extension = _extension_lower(file_name)
    return extension not in ignore and (_is_known_mime(file_name) or extension in files)


def _extension_lower(file_name):
    extension = os.path.splitext(file_name)[1]
    extension = extension[1:]
    return extension.lower() if extension else None
