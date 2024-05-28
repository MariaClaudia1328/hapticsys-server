# Hapticsys Server

## Description

<!-- TODO: give a better description -->
A server to receive and send hapticsys signals 

## Requirements

- Python 3.11
- Flask
- Linux 
- Python Virtual Env (venv)
- Pip

## Execution (via terminal)

1. Set Virtual Enviroment

```bash
mkdir env
cd env
sudo python3.11 -m venv env
source env/bin/activate
sudo pip install -r requirements.txt
```

2. Run server

```bash
flask run
```

3. Stop server and deactivate the virtual enviroment

```bash
# Stop flask process with [crtl+c]
deactivate
```

## Notes

- The system hasn't been tested on Windows or WSL
