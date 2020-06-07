#!/usr/bin/env bash

REPOSITORY_URL=https://cloudnativejava.jfrog.io/artifactory/api/pypi/pypi-local

rm -rf dist
rm -rf build
rm -rf simple_python_github_client.egg-info

pipenv install
pipenv install twine
pipenv run python setup.py sdist bdist_wheel
pipenv run twine check dist/*
pipenv run twine upload --verbose --non-interactive --repository-url ${REPOSITORY_URL} -u "$ARTIFACTORY_USERNAME" -p "$ARTIFACTORY_PASSWORD" dist/*
