#!/bin/bash


pip install selenium beautifulsoup4

if [ "$1" == "--site" ]; then
    if [ "$2" == "justremote" ]; then
        echo "Running JustRemote.com crawler..."
        python3 main.py --site justremote
    elif [ "$2" == "remote" ]; then
        echo "Running RemoteCom.com crawler..."
        python3 main.py --site remote
    else
        echo "Error: Invalid site option. Use '--site justremote' or '--site remote'."
        exit 1
    fi
else
    echo "Error: No site option provided. Use '--site justremote' or '--site remote'."
    exit 1
fi
