#!/bin/sh
echo -ne '\033c\033]0;Jumping Cookies\a'
base_path="$(dirname "$(realpath "$0")")"
"$base_path/jampjax.x86_64" "$@"
