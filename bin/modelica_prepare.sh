#! /usr/bin/env sh

apt update
apt install -y lsb-release

echo Linux name: `lsb_release --short --codename`
echo deb http://build.openmodelica.org/apt `lsb_release --short --codename` nightly | tee -a /etc/apt/sources.list.d/openmodelica.list
echo deb-src http://build.openmodelica.org/apt nightly contrib | tee -a /etc/apt/sources.list.d/openmodelica.list
wget -q http://build.openmodelica.org/apt/openmodelica.asc -O- | apt-key add -
apt-get update
apt-get build-dep -y openmodelica

apt-get -y install auditd
apt-get install --reinstall -y ca-certificates
update-ca-certificates
