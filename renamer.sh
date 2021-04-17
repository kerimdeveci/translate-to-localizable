#!/bin/sh
# This is a comment!
for i in $(find . -name "Localizable.strings" ); do
sed 's/% @/%@/' <<<"$(iconv -f ISO-8859-1 <<<$'voil\x{e0}')" | iconv -t ISO-8859-1
done