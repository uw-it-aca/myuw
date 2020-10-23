module.exports = {
  root: true,
  env: {
    // this section will be used to determine which APIs are available to us
    // (i.e are we running in a browser environment or a node.js env)
    'node': true,
    'browser': true,
    'jest/globals': true,
  },
  plugins: ['jest'],
  extends: [
    // use the recommended rule set for both plain javascript and vue
    'eslint:recommended',
    'google',
    'plugin:vue/recommended',
    'plugin:jest/recommended',
  ],
  rules: {
    // we should always disable console logs and debugging in production
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'max-len': ['error', { ignoreUrls: true, ignoreStrings: true }],
    'jest/no-disabled-tests': 'warn',
    'jest/no-focused-tests': 'error',
    'jest/no-identical-title': 'error',
    'jest/prefer-to-have-length': 'warn',
    'jest/valid-expect': 'error',
    'jest/expect-expect': [
      'error',
      {
        assertFunctionNames: ['expect*'],
      },
    ],
    // TODO: This is not ideal and needs to fixed at some point
    'vue/no-v-html': 'off',
    'vue/max-attributes-per-line': 'off',
  },
};
