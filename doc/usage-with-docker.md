.. _usage-with-docker:

# Usage with Docker
Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers. By using docker, you can ensure that your bot's environment is the same regardless of whether your bot is self-hosted, cloud hosted, or hosted anywhere else that supports docker.

### Install Docker
Start by installing Docker using the instructions provided on the [docker website](https://docs.docker.com/get-docker/).

### Prepare the bot code
After you have installed docker, you will next need to have the source code of your bot ready. For this example we will be using the echo bot from the [quickstart](quickstart.html).

### Write the Dockerfile
Docker uses instructions located within files with the name of "Dockerfile" (no file extension). A completed dockerfile will be provided at the end.

Create a file with a name of "Dockerfile", and without any file extension.
To begin the Dockerfile, we will need to set a base image. Docker will use this image as a starting point for our docker image during the build.
```
FROM python:latest
```
Python is preinstalled with this image, however the python packages needed will still need to be installed using the following line.
```
RUN python -m pip install simplematrixbotlib
```
Copy your bot's source code to the container using ADD. The first argument is the location in the host's filesystem, and the second argument is the location in the container's filesystem.
```
ADD echo.py echo.py
```
It will then be neccesary to set a command for docker to run when a docker image of the container is run. Use python as the command, and add any neccesary arguments using the same syntax as a python list of strings.
```
CMD [ "python", "echo.py" ]
```

### Build the Docker container
Before you can run the bot, docker will need to build a container using the Dockerfile. The syntax for this command is "docker build -t container name Directory with Dockerfile"
```
docker build -t echo-bot .
```

### Create and run Docker image

Docker will automatically create a Docker image from the container and run it when you use the following command.
```
docker run echo-bot
```
If you want to be able to view print output in your terminal or cmd prompt, then use the following command instead.
```
docker run -e PYTHONBUFFERED=1 echo-bot
```

This concludes this guide. More information on Docker can be found at [docker.com](docker.com) and more information on simplematrixbotlib can be found elsewhere in this documentation.