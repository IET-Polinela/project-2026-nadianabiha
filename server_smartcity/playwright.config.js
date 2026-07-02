const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: '../tests/e2e',
  reporter: [['html', { open: 'never' }], ['list']],
  globalSetup: require.resolve('../scripts/playwright-global-setup.js'),
  globalTeardown: require.resolve('../scripts/playwright-global-teardown.js'),
  use: {
    trace: 'on-first-retry',
  },
});
