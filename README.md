# Docker-On-Demand

Deploy docker containers from prebuilt images on demand.

## Configuration

+ `./server/config.py`

```python
PORT_START = 40000                                  # Random port range start
PORT_END = 60000                                    # Random port range end
APP_PORT = 5015                                     # Server port
HOST_IP = "http://challenge.host"                   # IP/Host of challenge server
SECRET = ""                                         # JWT Secret
challenges = json.load(open("challenges.json"))     # Do not change
```

+ Add entries to `./server/challenges.json` to add challenges.

```
{
    "<image_name>" : { 
        "local_port" : "<local_port>"
    } 
}
```

## Project Structure

```
docker-on-demand
├── config
│   └── dod.service
├── README.md
├── server
│   ├── app.py
│   ├── challenges.json
│   ├── config.py
│   ├── database.sqlite
│   ├── deployer.py
│   ├── requirements.txt
│   └── wsgi.py
└── tests
    ├── config.py
    ├── plugin.py
    └── requirements.txt
```
