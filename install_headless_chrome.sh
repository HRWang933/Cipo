#!/bin/bash
# from https://chromium.woolyss.com/
# and https://gist.github.com/addyosmani/5336747
# and https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:canonical-chromium-builds/stage
sudo apt-get update
sudo apt-get install chromium-browser 

#sudo apt-get install -y libglib2.0-0 \
#    libnss3 \
#    libgconf-2-4 \
#    libfontconfig1
#chromium-browser --headless --no-sandbox http://example.org/