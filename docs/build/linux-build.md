This instruction made for Ubuntu.

## Installation

Install all project:

```sh
git clone git@github.com:ostis-apps/nika.git
cd nika
git submodule update --init --recursive
cd scripts/
./install_deps_ubuntu.sh
./install_project.sh
```

Install Ubuntu dependencies:

```sh
./scripts/install_deps_ubuntu.sh
```

Update/Install submodules:

```sh
git submodule update --init --recursive
```

## Build
```sh
cd nika/scripts
./build_kb.sh
```

## Run on Linux

### Run server

```sh
cd nika/scripts
./run_sc_server.sh
```

## Run sc-web interface

```sh
cd nika/ostis-web-platform/scripts
./run_scweb.sh
```

Then open localhost:8000 in your browser.
![Run sc-server and sc-web screenshot](images/runScServerScWeb.png)
