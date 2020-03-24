#!/bin/bash

echo
echo "Checking for latest updates"
echo

# make sure you have the latest version
git pull &&

echo
echo "Building images"
echo

# build the images, and re-build them if you've run this before for clean slate
# https://docs.docker.com/compose/reference/build/
docker-compose build --no-cache &&

echo
echo "Build successful!"
echo
echo "Starting prototype. (Elasticsearch will take a brief moment to load)"
echo

# spin up both containers using those images and open the "interface" service interactively
# https://docs.docker.com/compose/reference/run/
docker-compose run interface

echo
echo "End of prototype. Tidying up."
echo

# tidy up
# https://docs.docker.com/compose/reference/down/
docker-compose down &&
docker image rm $(docker image ls --filter="label=sdproto=true" --quiet) &&

echo
echo "Tidying up complete!"
echo
