#!/usr/bin/env sh

# define a variable to sotre the output from copyq clipboard
output=$(copyq clipboard)
goldendict -s "$output"
