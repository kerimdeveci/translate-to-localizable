# Google Translate to Localizable.strings

This is the script that translates an array of english written texts to supported text and append the results to Localizable.strings file.

## Script Requirements

install python3 if not already installed

```shell
brew install python3
```

## Running Script

### Arguments

there are 2 arguments

1. `-i` or `--input_dir` : Base input directory that the holds all the localizable folders . Do not insert `lproj` folder here. pass the folder that holds all `lproj` folders inside it.

2. `-l` or `--list` : list of strings that to be translated. This will be the key valur in your localizable.strings file. Make sure to enter in English. every key word must be seperated with space . multiple words must be inside a `'` character.

## Running

run the script like so :

```shell
python3 translate.py -i [PATH_TO_FOLDER_THAT_HOLDS_LPROJ_FOLDERS] -l [TRANSLATION_TEXT]
```

eg:

```shell
python3 translate.py -i ~/Desktop/project/Localizations -l 'Hello World' Widgets 'UI Design'
```

and now script will make request to google translate itself, and write results to that language `Localizable.strings` file.

## Supported Languages 

- Arabic,
- Belarusian,
- Cambodian, 
- Czech, 
- Chinese (Simplified),
- Chinese (Traditional), 
- Dutch, 
- English, 
- French,
- German, 
- Hebrew, 
- Hungarian,
- Indonesian, 
- Italian,
- Japanese, 
- Korean,
- Malay,
- Norwegian, 
- Portuguese, 
- Portuguese (brazilian), 
- Polish, 
- Russian, 
- Romanian, 
- Thai,
- Turkish, 
- Swedish, 
- Spanish,
- Spanish (latin america)
- Ukrainian, 
- Vietnamese, 

## Adding Languages that not supported

open translate.py in any code editor. inside you will find a tuple array named `LANGS` just add your value to the end of array. Tuple's first item must be lproj folder name without lproj, second will be the google translate language key. you can find this value inside google translate url parameters

```url
https://translate.google.com/?sl=de&tl=ko&op=translate
```

| | |
|-| - |
| `sl=de` | start language de which is German |
| `tl=ko` | target language ko which is Korean |

eg:
korean localizations are represented as `ko.lproj` in Xcode
korean represented as `ko` in url parameter of google translate
so if you want to add korean append this line to LANGS array

```python
("ko" , "ko")
```

happy coding