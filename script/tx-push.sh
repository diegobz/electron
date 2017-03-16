#!/usr/bin/env bash

# Only run once, and only on master
echo $TRAVIS_JOB_NUMBER | grep "\.1$"
if [ $? -eq 0 ] && [ $TRAVIS_BRANCH == master ]
then
    echo "Updating fresh source files for translations in Transifex"
    pip install -U transifex-client
    tx init --host https://www.transifex.com --token $TRANSIFEX_TOKEN
    tx push --source -f --no-interactive
fi
