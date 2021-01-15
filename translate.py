import urllib.request
import urllib.parse
import re
import html
import os

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

TRANSLATE_ARRAY = ["Widgets",  "some text", "another text"]
FOLDER_PATH = 'Localizations'
LANGS = [  # tuple array ( [FOR_LPROJ_FOLDER_NAME] , [FOR_GOOGLE_TRANSLATE_QUERY] )
    ("tr-TR", "tr"),
    ("th", "th"),
    ("zh-Hans", "zh-CN"),
    ("vi", "vi"),
    ("pt", "pt"),
    ("ru", "ru"),
    ("id", "id"),
    ("es", "es"),
    ("ar", "ar"),
    ("ja", "ja"),
    ("fr", "fr"),
    ("de", "de"),
    ("en", "en")
]


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
        print(f" {lang[0]}")
        array2 = []
        for item in TRANSLATE_ARRAY:
            translation = translate(item, lang[1], "en")
            new_format = (f"\"{item}\" = \"{translation}\";")
            print(new_format)
            array2.append(new_format)
        array.append(array2)
        print("______________________")
        print("\n")
        return array


def translate_to_language(language):
    """Translates the given array to the target language 
    returns a translated arrray"""
    array2 = []
    for item in TRANSLATE_ARRAY:
        translation = translate(item, language, "en")
        new_format = (f"\"{item}\" = \"{translation}\";")
        print(new_format)
        array2.append(new_format)
    print("______________________\n")
    return array2


def does_key_exist_in_file(translate_result, full_file_path):
    """Returns boolean if the key existed in the file """
    with open(full_file_path, 'r', encoding='utf-16') as file:
        # file.seek(0)
        lines = file.read()
        key = translate_result.split("=")[0]
        if key in lines:
            return True
        return False


def write_results_in_file(translate_results):
    """ writes the translation results to Localizable.string"""
    file_path = FOLDER_PATH + '/' + language_folder + '/' + "Localizable.strings"
    try:
        with open(file_path, 'a+', encoding='utf-16') as file:
            for t_result in translate_results:
                if does_key_exist_in_file(t_result, file_path) == True:
                    continue
                file.write(f'{t_result}\n')
    except IOError:
        print('File Write not Success')


if __name__ == "__main__":
    for language_folder in os.listdir(FOLDER_PATH):
        for script_lang in sorted(LANGS):
            language_name = os.path.splitext(language_folder)[0]
            if language_name in script_lang[0]:
                print(language_name)
                values = translate_to_language(script_lang[1])
                write_results_in_file(values)
