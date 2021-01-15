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
    'plugin:vue/recommended',
    'plugin:jest/recommended',
    'prettier',
    'prettier/vue',
  ],
  parserOptions: {
    parser: 'babel-eslint',
  },
  rules: {
    // global rules
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    // TODO: Remove this rule
    'no-unused-vars': 'off',
    "camelcase": [2, {"properties": "never"}],
    'max-len': [
      2,
      {
        code: 100,
        tabWidth: 2,
        ignoreUrls: true,
        ignoreStrings: true,
        ignoreTemplateLiterals: true,
      },
    ],
    // jest rules
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
    // vue
    'vue/no-mutating-props': 'off',
    'vue/no-v-html': 'off',
    'vue/max-attributes-per-line': 'off',
  },
};
