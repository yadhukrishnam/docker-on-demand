# Docker-On-Demand

Deploy docker containers from prebuilt images on demand.

## Configuration

+ config.py 

```python
PORT_START = 40000                                  # Random port range start
PORT_END = 60000                                    # Random port range end
APP_PORT = 5015                                     # Server port
HOST_IP = "http://web.challenge.bi0s.in"            # IP/Host of challenge server
CLIENT_IP = ""                                      # 
SECRET = ""                                         # JWT Secret
challenges = json.load(open("challenges.json"))     # Do not change
```

+ Add entries to challenges.json to add challenges.

```
{
    "<image_name>" : { 
        "local_port" : "<local_port>"
    } 
}
```
