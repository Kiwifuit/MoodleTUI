#!/usr/bin/env sh
# TODO: Port this script to Batch/Powershell

source venv/run/bin/activate
mkdir build

# Push requirements to file
pip freeze > requirements.txt

# Build source tarballs
tar vczf build/MoodleTUI-$1-src.tar.gz src/**/*
tar vczf build/MoodleTUI-$1-res.tar.gz res/**/*

# Build Docker Image
docker image rm -f python:3.10.4-alpine
docker image rm -f moodletui:$1
docker build -t moodletui .

# Grab Image
docker save -o build/MoodleTUI-$1-docker.tar moodletui:$1

# Build Executable
nuitka3 --standalone --onefile --include-plugin-directory=./src/ -o build/MoodleTUI src/main.py

# Build Nuitka output tarballs
tar vczf build/MoodleTUI-$1-nuitka-build.tar.gz main.build/**
tar vczf build/MoodleTUI-$1-nuitka-dist.tar.gz main.dist/**

# Remove Nuitka Dist and Build files
rm -vrf main.dist/
rm -vrf main.build/