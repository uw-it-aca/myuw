FROM cypress/browsers:node12.18.3-chrome87-ff82

WORKDIR /
RUN mkdir e2e

ADD --chown=node:node ./package.json /e2e/package.json

WORKDIR /e2e
RUN npm install .

ADD --chown=node:node ./cypress /e2e/cypress
ADD --chown=node:node ./cypress.json /e2e/cypress.json

ENTRYPOINT [ "/e2e/node_modules/.bin/cypress", "run" ]