/// <reference types="cypress" />
const { startDevServer } = require('@cypress/webpack-dev-server')
const webpackConfig = require('./../../webpack.cypress.config')

/**
 * @type Cypress.PluginConfig
 */
module.exports = (on, config) => {
  on('dev-server:start', (options) => {
    return startDevServer({
      options,
      webpackConfig,
    })
  })

  on('task', {
    log (message) {
      console.log(message)
      return null
    }
  })

  require('@cypress/code-coverage/task')(on, config)

  return config
}