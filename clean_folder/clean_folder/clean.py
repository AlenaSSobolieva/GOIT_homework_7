from pathlib import Path
import shutil
import sys
import re


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
LATIN_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANSLITERATION = {}

for cs, ls in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):
    TRANSLITERATION[ord(cs)] = ls # for small leters
    TRANSLITERATION[ord(cs.upper())] = ls.upper() # for capital letters

def normalize(name: str) -> str:
    transliterated_name = name.translate(TRANSLITERATION) # for small and capital letters
    transliterated_name = re.sub(r'\W', '_', transliterated_name)

    return transliterated_name


JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_MUSIC = []
OGG_MUSIC = []
WAV_MUSIC = []
AMR_MUSIC = []
ZIP_ARCHIVE = []
GZ_ARCHIVE = []
TAR_ARCHIVE = []
MY_OTHERS = []

REGISTERED_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_MUSIC,
    'OGG': OGG_MUSIC,
    'WAV': WAV_MUSIC,
    'AMR': AMR_MUSIC,
    'ZIP': ZIP_ARCHIVE,
    'GZ': GZ_ARCHIVE,
    'TAR': TAR_ARCHIVE,
}

FOLDERS = []
EXTENSIONS = set()  # only unique
UNDEFINED = set()  # only unique

def define_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()  # without fullstop and in capital letters
def scanning(folder: Path) -> None:
    for el in folder.iterdir():
        if el.is_dir():
            if el.name not in ('archives', 'video', 'audio', 'documents', 'images', 'other files'):
                FOLDERS.append(el)
                scanning(el)
            continue

        ext = define_extension(el.name)
        fullname = folder / el.name

        if not ext:
            MY_OTHERS.append(fullname)

        else:
            try:
                container = REGISTERED_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                UNDEFINED.add(ext)
                MY_OTHERS.append(fullname)

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))
def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))
def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)

    try:
        shutil.unpack_archive(filename, folder_for_file)
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    filename.unlink()
def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Can not delete this folder: {folder}')
def main(folder: Path):
    scanning(folder)

    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX')

    for file in MP3_MUSIC:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_MUSIC:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in WAV_MUSIC:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in AMR_MUSIC:
        handle_media(file, folder / 'audio' / 'AMR')

    for file in MY_OTHERS:
        handle_other(file, folder / 'other files')

    for file in ZIP_ARCHIVE:
        handle_archive(file, folder / 'archives' / 'ZIP')
    for file in GZ_ARCHIVE:
        handle_archive(file, folder / 'archives' / 'GZ')
    for file in TAR_ARCHIVE:
        handle_archive(file, folder / 'archives' / 'TAR')

    for folder in FOLDERS[::-1]:
        handle_folder(folder)

def start():
    try:
        if sys.argv[1]:
            folder_for_scan = Path(sys.argv[1])
            print(f'Start in folder: {folder_for_scan}')
            main(folder_for_scan)
    except IndexError as err:
        print(f'You should enter the name of directory to clean it.')

if __name__ == '__main__':
    try:
        if sys.argv[1]:
            folder_for_scan = Path(sys.argv[1])
            print(f'Start in folder: {folder_for_scan}')
            main(folder_for_scan)
    except IndexError as err:
        print(f'You should enter the name of directory to clean it.')



