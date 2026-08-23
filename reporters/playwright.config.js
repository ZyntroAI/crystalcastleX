import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: [
    ['list'],
    ['./reporters/githubTriggerReporter.js'],
  ],
});
