#!/bin/bash
set -e

g++ -O2 -o solution solution.cpp

if [ $? -ne 0 ]; then
    exit 1
fi

./solution < input.txt
