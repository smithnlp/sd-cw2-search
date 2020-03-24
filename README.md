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
Once you've completed the set up, run the following whenever you want to launch the interactive search prototype.
```shell
./run_prototype.sh
```

## TODO
- [x] actual instructions including to install docker and docker-compose
- [x] maybe do these all as one bash script with conditional &&s etc.
- [ ] document each file
