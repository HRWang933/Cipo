#You need to add the following entries to /etc/apt/sources.list or a new file in /etc/apt/sources.list.d/:
sudo echo "" >> /etc/apt/sources.list
sudo echo "# TOR Packages" >> /etc/apt/sources.list
sudo echo "deb https://deb.torproject.org/torproject.org xenial main" >> /etc/apt/sources.list
sudo echo "deb-src https://deb.torproject.org/torproject.org xenial main" >> /etc/apt/sources.list

sudo apt-get install apt-transport-https
sudo gpg2 --recv A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89
sudo gpg2 --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -
sudo apt-get update
sudo apt-get install tor deb.torproject.org-keyring