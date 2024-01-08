# Hapticsys Server

## Description

<!-- TODO: give a better description -->
A server to receive and send hapticsys signals 

## Requirements

- Python >= 3.0.0
- Flask [latest]
- Linux 

## Execution (via terminal)

1. Set Virtual Enviroment

```bash
sudo pacman -S python-virualenv
sudo pacman -S python-pip
mkdir env
cd env
sudo python -m venv env
source flaskenv/bin/activate
sudo pip install -r requirements.txt

```

2. Run server

```bash
flask run
```

3. Stop server and deactivate the virtual enviroment

```bash
# Usar [crtl+c]
deactivate
```

## Notes

- The system hasn't been tested on Windows or WSL
