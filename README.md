# Docker-On-Demand

Docker-on-demand is an API for dynamically deploying and managing docker containers from docker images. 

This can be easily integrated with Capture-The-Flag frameworks like [CTFd](https://github.com/CTFd/CTFd) to provide dynamic challenge deployment. 

## Getting Started

### Installation

```bash
git clone https://github.com/yadhukrishnam/docker-on-demand
cd docker-on-demand
pip3 install -r requirements.txt
```

### Configuration

Make changes to `server/config/config.yaml` to configure the application. An example configuration is given below. 

```yaml
version: 1.0

images:
  myimage: #image name
    local_port: 8080 # internal port

app_conf:
  port_start: 40000 # random port start value
  port_end: 60000 # random port end value
  app_port: 5015 # API port
  host: "http://127.0.0.1" # front-end host
  debug: False # Flask Debug mode

# Username : Password for API dashboard
credentials:
  admin: admin 
  user: user
```

## Features

+ Deploy docker container on user demand.
+ Easy-to-use API to deploy and kill docker containers.
+ Dynamic port allocation for instances.
+ Admin dashboard to manage all deployments.
+ Automatic docker termination after certain interval.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch.
3. Commit your Changes.
4. Push to the Branch.
5. Open a Pull Request


## License

Distributed under the MIT License. See LICENSE for more information.