# sd-cw2-search
Coursework 2 prototype submission for Software Development INFR11172.

## Set-up
You only need to do these steps once.

---
If you don't have `docker` and/or `docker-compose` on your machine, you'll need those before doing anything else. To check if you have them already:
```shell
docker --version
```
```shell
docker-compose --version
```
Otherwise, follow [these instructions to install Docker](https://docs.docker.com/install/) and [these to install Docker Compose](https://docs.docker.com/compose/install/) according to your machine and operating system.

---

Clone this repository, go into the directory, and make the main shell script executable.
```shell
git clone https://github.com/smithnlp/sd-cw2-search.git
cd sd-cw2-search
chmod +x run_prototype.sh
```

## Usage
Once you've completed the set up, run the following whenever you want to launch the interactive search prototype. Take a peek inside `run_prototype.sh` if you'd like; it is a simple shell script which pulls the latest updates from this repository, builds the container images, and then runs the services as coordinated by `docker-compose.yml` but in such a way that we interact directly with the `interface` container. When you're done using the prototype, it shuts down the containers and deletes the corresponding images from your machine.

- When you run the following, you will see lots of output to the console logging the build process.
- Eventually, the prototype will be opened with a welcome message. Type queries as if it were a normal search bar in a website and upon entering you will enter a [`less`](https://en.wikipedia.org/wiki/Less_(Unix)) window with the results.
- Press `q` to return to the search bar interface.
- The database is very small for the purposes of this prototype, so take a look at `interace/games.csv` in this repository for an idea of what kinds of searches you might try.
- When completely done using the prototype, type `exit` as a search and everything should gracefully shut down.

```shell
./run_prototype.sh
```
