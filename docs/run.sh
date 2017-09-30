#! /bin/sh

unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
  alias uopen='xdg-open'
elif [[ "$unamestr" == 'Darwin' ]]; then
  alias uopen='open'
fi

uopen "http://localhost:8000/docs/puzzles_spec.html"
python -m http.server
