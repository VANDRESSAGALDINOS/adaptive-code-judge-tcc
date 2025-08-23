#!/bin/bash
set -e

# Compile C++ code
echo "Compiling C++ code..."
g++ -O2 -o solution solution.cpp

if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

echo "Compilation successful"

# Run the compiled program
echo "Running solution..."
./solution < input.txt
