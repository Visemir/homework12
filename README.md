docker-compose.yml

Part 1

Create a [docker-compose.yml](https://github.com/Visemir/homework12/blob/main/docker-compose.yml) file based on [Homework 11.](https://github.com/Visemir/homework12/tree/main/app)

In this file, you need to set up a service called app using the Docker image from Homework 11. 

The Docker image for app should be built dynamically using docker-compose.

Part 2

In addition, set up an nginx service and configure it as a reverse proxy to the app service, handling requests on HTTP port 8080. 

The nginx configuration should be located at [/etc/nginx/conf.d/default.conf](https://github.com/Visemir/homework12/blob/main/nginx/default.conf) inside the container.

As a result, you should push your [docker-compose.yml](https://github.com/Visemir/homework12/blob/main/docker-compose.yml), [nginx configuration file](https://github.com/Visemir/homework12/blob/main/nginx/default.conf), source code of your [application](https://github.com/Visemir/homework12/blob/main/app/app.py) and screenshots demonstrating that the setup works (e.g., a successful request made to the nginx proxy).

![](https://github.com/Visemir/homework12/blob/main/site.jpg)
