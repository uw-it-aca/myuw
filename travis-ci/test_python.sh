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

run_test "pycodestyle ${DJANGO_APP}/ --exclude=migrations,static"

# template compress mistakes
run_test "grep -re '<\s*/\s*br\s*>' myuw/templates/ ; test \$? -eq 1 &&\
          grep -r 'static/' myuw/ | grep -v /test/ | grep -v /tests/ | grep -v washington.edu/static; test \$? -eq 1"

run_test "FORCE_VIEW_TESTS=1 coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

# put generaged coverage result where it will get processed
cp .coverage.* /coverage
# cp coverage/lcov.info /coverage

exit 0
