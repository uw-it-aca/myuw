#!/bin/sh
set -e
trap 'exit 1' ERR

# travis test script for django app
#
# PRECONDITION: inherited env vars from application's .travis.yml MUST include:
#      DJANGO_APP: django application directory name

# start virtualenv
source bin/activate

# install test tooling
pip install pycodestyle coverage
apt-get install -y nodejs npm rubygems
npm install -g jshint
npm install -g jquery
npm install -g moment
npm install -g moment-timezone
npm install -g datejs
npm install -g jshint
npm install -g mocha
npm install -g nyc
npm install -g jsdom@15.2.1
npm install -g sinon
npm install coveralls
gem install coveralls-lcov

function run_test {
    echo "##########################"
    echo "TEST: $1"
    eval $1
}

run_test "pycodestyle ${DJANGO_APP}/ --exclude=migrations,static"

# template compress mistakes
run_test "grep -re '<\s*/\s*br\s*>' myuw/templates/ ; test \$? -eq 1 && grep -r 'static/' myuw/ | grep -v /test/ | grep -v washington.edu/static; test \$? -eq 1"

if [ -d ${DJANGO_APP}/static/${DJANGO_APP}/js ]; then
    run_test "jshint ${DJANGO_APP}/static/${DJANGO_APP}/js --verbose"
elif [ -d ${DJANGO_APP}/static/js ]; then
    run_test "jshint ${DJANGO_APP}/static/js --verbose"
fi

run_test 'mocha myuw/static/js/test/ --recursive'

run_test 'nyc --include-all-sources -x "**/vendor/**" -x "**/site-packages/**" _mocha -- -R spec myuw/static/js/test/'

run_test "FORCE_VIEW_TESTS=1 coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

run_test "coveralls-lcov -v -n coverage/lcov.info > js-coverage.json"

# put generaged coverage result where it will get processed
cp .coverage.* /coverage
cp js-coverage.json

exit 0
