#!/bin/bash
pip3 install pipenv
pipenv install
pipenv run gunicorn app:app