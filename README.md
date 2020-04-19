![last update](http://yourgitlabuser.gitlab-pages.saarsec.rocks/yourservicename/ci-update.svg)
![pipeline status](https://gitlab.saarsec.rocks/YourGitlabUser/yourservicename/badges/master/pipeline.svg)
![build](http://yourgitlabuser.gitlab-pages.saarsec.rocks/yourservicename/ci-build.svg)
![install](http://yourgitlabuser.gitlab-pages.saarsec.rocks/yourservicename/ci-install.svg)
![checkers](http://yourgitlabuser.gitlab-pages.saarsec.rocks/yourservicename/ci-checkers.svg)
![exploits](http://yourgitlabuser.gitlab-pages.saarsec.rocks/yourservicename/ci-exploits.svg)

`TODO` please edit logo URLs (above) after fork to get badges working


saarCTF Example Service
=======================

Want to create a service?
-------------------------
Follow these [instructions from the gamelib manual](https://github.com/MarkusBauer/saarctf-gamelib/blob/master/README.md)

Basics
------
Create your service project in `./service/`.
 
Basic rules: After fork you can edit everything here except the `gamelib` folder.


How to rename this service
--------------------------
1. Edit `./servicename`
2. Edit `./docker-compose.yml`

How to configure build and installation
---------------------------------------
Your service will be "build" locally. The result of "build" is copied to the vulnbox (not the service itself).
On the vulnbox it will then be "install"ed. 

You can script build and install steps in `./build.sh` and `./install.sh`. See [the gamelib manual](https://github.com/MarkusBauer/saarctf-gamelib/blob/master/docs/howto_build_install.md) for instructions.


How to write checker scripts
----------------------------
1. Create a python3 file in `./checkers/`
2. Create a file `./checkers/config` with content `<filename>:<classname>`. 
3. Hack on! See [the gamelib manual](https://github.com/MarkusBauer/saarctf-gamelib/blob/master/docs/howto_checkers.md) for details how your python script should look like.


How to write exploits
---------------------
1. Create a python3 script in `./exploits/` named `exploit_<???>.py`
2. Code it (see example exploit there, or [the gamelib manual](https://github.com/MarkusBauer/saarctf-gamelib/blob/master/docs/howto_exploits.md))


How to test things
------------------
Preferably in this order, run:
- `gamelib/run-build` - build the service (test `build.sh`) and store output in `./build_output`
- `gamelib/run-install` - create a docker image containing your service (test `install.sh`)
- `docker-compose up [-d]` - start a container with your service image to test against
  - use `-d` to start in detached mode
  - the container writes his IPs to `./docker-container-infos.txt` once started
- `gamelib/run-checkers` - run unit tests against your checker script to find basic errors. Service docker container must be running.
- `gamelib/run-exploits` - test your exploits against your service docker container.


How to do Continous Integration
-------------------------------
1. Push your service to saarsec Gitlab
2. Test `build` and `install` steps locally
3. Notify an admin that enables the CI for your project
4. In your very first pipeline, trigger the `build-base-image` step by hand (necessary only once)
