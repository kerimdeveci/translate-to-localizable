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

2. `-l` or `--list` : list of strings that to be translated. every key word must be seperated with space . multiple words must be inside a `'` character.

## Running

run the script like so :

```shell
python3 translator.py -i [PATH_TO_FOLDER_THAT_HOLDS_LPROJ_FOLDERS] -i [TRANSLATION_TEXT]
```

eg:

```shell
python3 json-creator.py -i ~/Desktop/project/Localizations -i 'Hello World' Widgets 'UI Design'
```

and now script will make request to google translate itself, and write results to that language `Localizable.strings` file.

happy coding
