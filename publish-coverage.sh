#!/usr/bin/env bash

python -m pytest --basetemp=ttt --cov
python -m coverage report -m
python -m coverage xml
python-codacy-coverage -r coverage.xml