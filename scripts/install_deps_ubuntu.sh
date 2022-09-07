#!/usr/bin/env bash
packagelist=(
	python3-pip
	python3-setuptools
	build-essential
	cmake
	nlohmann-json3-dev
)
sudo apt-get install -y --no-install-recommends "${packagelist[@]}"
