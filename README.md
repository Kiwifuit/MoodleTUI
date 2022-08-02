# cit-lair-tui
A Terminal interface for the Moodle LMS

# Table of Contents
- [cit-lair-tui](#cit-lair-tui)
- [Table of Contents](#table-of-contents)
- [Run](#run)
  - [Docker](#docker)
  - [Native](#native)

# Run
## Docker
**NOTE: This method is 100% untested due to the fact that this project reads on the disk**

Advantages:
* Python is not required
* All-in-one container

Disadvantages:
* Not tested yet

```
$ docker run misery/MoodleTUI
```
## Native
Advantages:
* Transpiles to C
* Outputs one binary executable
* Builds source code and resources in tarballs

Disadvantages:
* Might take forever
* Unix systems only for now
  * If you can port the `build.sh` file successfully, please do, I would appreciate that

```
$ chmod u+x build.sh
$ ./build.sh
```

<!--
# Downloading
If you want to download the source code:

## With `git`
```
$ git clone https://github.com/kiwifuit/MoodleTUI.git
$ cd MoodleTUI
```

## With `curl`
```
$ curl -q  -->
