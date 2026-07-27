import { expect, test } from '@playwright/test';

// E2E covers the money path only — the flow whose breakage makes the product
// worthless. Keep this set small and stable.
test('the home page renders and shows the item form', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Boilerplate' })).toBeVisible();
  await expect(page.getByPlaceholder('New item name')).toBeVisible();
});
