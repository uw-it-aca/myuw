#!/bin/sh
trap catch ERR

# travis test script for django app
#
# PRECONDITIONS:
#      * necessary test tooling already installed
#      * inherited env vars from application's .travis.yml MUST include:
#        DJANGO_APP: django application directory name

# start virtualenv
source bin/activate

function run_test {
    echo "##########################"
    echo "TEST: $1"
    eval $1
}

function catch {
    echo "Test failure occurred on line $LINENO"
    exit 1
}

run_test "FORCE_VIEW_TESTS=1 python -Wd -m coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

echo "pwd"
pwd

echo "ls -al"
ls -al

echo "ls -al /coverage"
ls -al /coverage

# put generaged coverage result where it will get processed
echo "cp .coverage.* /coverage"
cp .coverage.* /coverage
# cp coverage/lcov.info /coverage

ls -al /coverage

echo "ls /coverage"
ls -al /coverage

exit 0
