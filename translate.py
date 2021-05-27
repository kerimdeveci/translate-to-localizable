import urllib.request
import urllib.parse
import re
import html
import os
import codecs
import argparse

agent = {'User-Agent':
         "Mozilla/4.0 (\
compatible;\
MSIE 6.0;\
Windows NT 5.1;\
SV1;\
.NET CLR 1.1.4322;\
.NET CLR 2.0.50727;\
.NET CLR 3.0.04506.30\
)"}

TRANSLATE_ARRAY = [
    "App, needs to access your gallery to add wallpaper",
]
FOLDER_PATH = '/Users/kerimdeveci/Desktop/phone-color-screen/wallpix-shared/Localizations'
LANGS = [  # tuple array ( [FOR_LPROJ_FOLDER_NAME] , [FOR_GOOGLE_TRANSLATE_QUERY] )
    ("ar", "ar"),
    ("be-BY", "be"),
    ("km", "km"),
    ("cs-CZ", "cs"),
    ("zh-Hans", "zh-CN"),
    ("zh-Hant", "zh-TW"),
    ("nl", "nl"),
    ("en", "en"),
    ("fr", "fr"),
    ("de", "de"),
    ("he", "iw"),
    ("hu-HU", "hu"),
    ("id", "id"),
    ("it", "it"),
    ("ja", "ja"),
    ("ko", "ko"),
    ("ms", "ms"),
    ("nb", "no"),
    ("pt-BR", "pt"),
    ("pt-PT", "pt"),
    ("pl", "pl"),
    ("ru", "ru"),
    ("ro", "ro"),
    ("th", "th"),
    ("tr-TR", "tr"),
    ("tr", "tr"),
    ("sv", "sv"),
    ("es", "es"),
    ("es-419", "es"),
    ("uk", "uk"),
    ("vi", "vi"),
    ("ko", "ko"),
    ("Base", "en")
]


def detect_encoding(full_file_path):
    with open(full_file_path, 'rb') as file:
        s = file.readline()
    if s.startswith(codecs.BOM_UTF16_BE):
        return 'utf-16-be'
    if s.startswith(codecs.BOM_UTF16_LE):
        return 'utf-16-le'
    if s.startswith(codecs.BOM_UTF32_BE):
        return 'utf-32-be'
    if s.startswith(codecs.BOM_UTF32_LE):
        return 'utf-32-le'
    if s.startswith(codecs.BOM_UTF8):
        return 'utf-8'
    m = re.match(br'\s*<\?xml\b.*\bencoding="([^"]+)"', s)
    if m:
        return m.group(1).decode()
    m = re.match(br"\s*<\?xml\b.*\bencoding='([^']+)'", s)
    if m:
        return m.group(1).decode()
    # No encoding found -- what should the default be?
    return 'utf-8'


def translate(to_translate, to_language="auto", from_language="auto"):
    """Returns the translation using google translate
    you must shortcut the language you define
    (French = fr, English = en, Spanish = es, etc...)
    if not defined it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?
    """
    base_link = "https://translate.google.com/m?tl=%s&sl=%s&q=%s"
    to_translate = urllib.parse.quote(to_translate)
    link = base_link % (to_language, from_language, to_translate)
    request = urllib.request.Request(link, headers=agent)
    raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = html.unescape((re_result[0]))
    return (result)


def print_to_output():
    """this is for copy paste and debugging not using in this script"""
    array = []
    for lang in sorted(LANGS):
        print("______________________")
        print(f"translating to {lang[0]}")
        array2 = []
        for item in TRANSLATE_ARRAY:
            translation = translate(item, lang[1], "en")
            new_format = (f"\"{item}\" = \"{translation}\";")
            print(new_format)
            array2.append(new_format)
        array.append(array2)
        print("______________________\n")
        return array


def translate_array_to_language(language):
    """Translates the given array to the target language 
    returns a translated arrray"""
    array2 = []
    for item in TRANSLATE_ARRAY:
        translation = translate(item, language, "en")
        new_format = (f"\"{item}\" = \"{translation}\";")
        print(new_format)
        array2.append(new_format)
    return array2


def does_key_exist_in_file(translate_result, full_file_path):
    """Returns boolean if the key existed in the file """
    encoding = detect_encoding(full_file_path)
    with open(full_file_path, 'r', encoding=encoding) as file:
        file.seek(0)
        lines = file.read()
        key = translate_result.split("=")[0]
        if key in lines:
            print(f"the key: {key} is already exists skipping writing")
            return True
        return False


def write_results_in_file(translate_results, folder):
    """ writes the translation results to Localizable.string"""
    file_path = FOLDER_PATH + '/' + folder + '/' + "InfoPlist.strings"
    try:
        encoding = detect_encoding(file_path)
        with open(file_path, 'a+', encoding=encoding) as file:
            print("\n")
            for t_result in translate_results:
                if does_key_exist_in_file(t_result, file_path) == True:
                    continue
                file.write(f'{t_result}\n')
                print(f"Writing {t_result} to file {file_path} ...")

    except IOError:
        print('File Write not Success')


if __name__ == "__main__":

    dir = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input_dir',
        help='Full Output Path eg: Users/[username]/Desktop/StickerCategories')

    parser.add_argument("-l", "--list", nargs="+",
                        default=["Show Offer", "Continue"])

    args = parser.parse_args()

    if args.input_dir:
        FOLDER_PATH = args.input_dir
    else:
        FOLDER_PATH = dir

    if args.list:
        TRANSLATE_ARRAY = args.list

    for language_folder in os.listdir(FOLDER_PATH):
        for script_lang in sorted(LANGS):
            language_name = os.path.splitext(language_folder)[0]
            if language_name in script_lang[0]:
                print(f"translating to {language_name}  ==> \n")
                values = translate_array_to_language(script_lang[1])
                write_results_in_file(values, language_folder)
                print("______________________\n")
