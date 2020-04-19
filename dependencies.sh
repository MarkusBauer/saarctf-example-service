#!/usr/bin/env bash

set -eux

# Install all your checkerscript / exploit dependencies
# Please prefer Debian packages over pip (for stability reasons)
# OS will be Debian Buster.
# Already installed python modules are:
# - redis
# - requests
# - pwntools
# - numpy
# - pycryptodome
# - psutil
# - bs4
# - pytz

# uncomment for APT
# apt update
# apt install -y python3-requests

# uncommnent for pip
# python3 -m pip install requests
