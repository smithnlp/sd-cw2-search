#!/bin/bash

echo
echo "--------------------------------------------------------------------------------"
echo "Checking for latest updates"
echo "--------------------------------------------------------------------------------"
echo

# make sure you have the latest version
git pull &&

echo
echo "--------------------------------------------------------------------------------"
echo "Building images"
echo "--------------------------------------------------------------------------------"
echo

# build the images, and re-build them if you've run this before for clean slate
# https://docs.docker.com/compose/reference/build/
docker-compose build --no-cache &&

echo
echo "--------------------------------------------------------------------------------"
echo "Build successful!"
echo "--------------------------------------------------------------------------------"
echo
echo "--------------------------------------------------------------------------------"
echo "Starting prototype. (Elasticsearch will take a brief moment to load)"
echo "--------------------------------------------------------------------------------"
echo

# spin up both containers using those images and open the "interface" service interactively
# https://docs.docker.com/compose/reference/run/
docker-compose run interface

echo
echo "--------------------------------------------------------------------------------"
echo "End of prototype. Tidying up."
echo "--------------------------------------------------------------------------------"
echo

# tidy up
# https://docs.docker.com/compose/reference/down/
docker-compose down &&
# also, delete the images because it's likely you don't want them taking up space after a single use
# use a special label added within the Dockerfiles to easily find them and remove
docker image rm $(docker image ls --filter="label=sdproto=true" --quiet) &&

echo
echo "--------------------------------------------------------------------------------"
echo "Tidying up complete!"
echo "--------------------------------------------------------------------------------"
echo
