#!/bin/bash

# make sure you have the latest version
git pull &&

# build the images, and re-build them if you've run this before for clean slate
# https://docs.docker.com/compose/reference/build/
docker-compose build --no-cache &&

# spin up the containers using those images and open the interface service interactively
# https://docs.docker.com/compose/reference/run/
docker-compose run interface

# clean up
# https://docs.docker.com/compose/reference/down/
docker-compose down &&
docker image rm $(docker image ls --filter="label=sdproto=true" --quiet)
