#!/bin/sh
if pgrep "dropbox" > /dev/null
then
echo ""
else
~/.dropbox-dist/dropboxd
fi

sudo python server.py
