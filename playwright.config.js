const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    trace: 'on-first-retry',
  },
});
