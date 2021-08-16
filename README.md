# Docker-On-Demand

Deploy docker containers from prebuilt images on demand.

## Configuration

+ `./server/config.py`

```python
PORT_START = 40000                                  # Random port range start
PORT_END = 60000                                    # Random port range end
APP_PORT = 5015                                     # Server port
HOST_IP = "http://image.host"                       # IP/Host of image server
SECRET = ""                                         # JWT Secret
```

+ Add entries to `./server/images.json` to add images.

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
│   ├── images.json
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
