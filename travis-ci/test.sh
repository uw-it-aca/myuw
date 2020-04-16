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
          grep -r 'static/' myuw/ | grep -v /test/ | grep -v washington.edu/static; test \$? -eq 1"

if [ -d ${DJANGO_APP}/static/${DJANGO_APP}/js ]; then
    run_test "jshint ${DJANGO_APP}/static/${DJANGO_APP}/js --verbose"
elif [ -d ${DJANGO_APP}/static/js ]; then
    run_test "jshint ${DJANGO_APP}/static/js --verbose"
fi

run_test 'nyc mocha  --recursive myuw/static/js/test/'

run_test "FORCE_VIEW_TESTS=1 coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

run_test "coveralls-lcov -v -n coverage/lcov.info > /coverage/js-coverage.json"

# put generaged coverage result where it will get processed
cp .coverage.* /coverage

exit 0
