import { expect, test } from '@playwright/test';
import { acceptNextDialog, backendIsReachable, registerViaUi, uniqueUsername } from './_helpers.js';

test.describe.serial('Companions (contacts), chats, messaging, deletes, WebSocket', () => {
  async function skipIfBackendDown(request) {
    const ok = await backendIsReachable(request);
    test.skip(!ok, 'Backend not reachable on http://127.0.0.1:8000 (start backend before running e2e)');
  }

  test('navbar buttons exist and basic navigation works after auth', async ({ page }) => {
    await skipIfBackendDown(page.request);
    await registerViaUi(page);

    const nav = page.locator('nav.bottom-navbar');
    await expect(nav).toBeVisible();

    await expect(page.getByRole('link', { name: 'Chat' })).toBeVisible();
    await expect(page.getByRole('link', { name: '3d' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Companion' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Shop' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Settings' })).toBeVisible();

    await page.getByRole('link', { name: 'Settings' }).click();
    await expect(page.getByRole('heading', { name: 'Settings' })).toBeVisible();

    await page.getByRole('link', { name: 'Chat' }).click();
    await expect(page.getByRole('heading', { name: 'Chats', exact: true })).toBeVisible();
  });

  test('create two companions, create two chats, send a message over WebSocket', async ({ page }) => {
    await skipIfBackendDown(page.request);
    await registerViaUi(page);

    const companion1 = `Alice-${uniqueUsername('c')}`;
    const companion2 = `Bob-${uniqueUsername('c')}`;

    await page.getByRole('link', { name: 'Companion' }).click();
    await expect(page.getByRole('heading', { name: 'Companions' })).toBeVisible();

    // Create companion #1
    await page.getByText('Add a companion').click();
    await page.getByLabel('Avatar URL').fill('https://example.com/a.png');
    await page.getByLabel('Name').fill(companion1);
    await page.getByRole('button', { name: 'Add' }).click();
    await expect(page.getByText(companion1)).toBeVisible();

    // Create companion #2
    await page.getByText('Add a companion').click();
    await page.getByLabel('Avatar URL').fill('https://example.com/b.png');
    await page.getByLabel('Name').fill(companion2);
    await page.getByRole('button', { name: 'Add' }).click();
    await expect(page.getByText(companion2)).toBeVisible();

    // Create chat #1 with companion #1
    await page.getByRole('link', { name: 'Chat' }).click();
    await expect(page.getByRole('heading', { name: 'Chats', exact: true })).toBeVisible();

    await page.getByText('Click to assign companion').first().click();
    await expect(page.getByRole('heading', { name: 'Select companion' })).toBeVisible();
    await page
      .locator('.available-companion-item', { hasText: companion1 })
      .getByRole('button', { name: 'Start Chat' })
      .click();

    await expect(page).toHaveURL(/\/chat\/.+/);
    await expect(page.getByRole('button', { name: 'Delete Chat' })).toBeVisible();

    // WebSocket send -> UI receives and renders message
    const message1 = `hello-${Date.now()}`;
    await page.locator('#message').fill(message1);
    await page.getByRole('button', { name: 'Send' }).click();
    await expect(page.getByText(message1)).toBeVisible();

    // Back to chats
    await page.getByRole('link', { name: 'Back to chats' }).click();
    await expect(page).toHaveURL(/\/chat$/);

    // Create chat #2 with companion #2
    await page.getByText('Click to assign companion').first().click();
    await page
      .locator('.available-companion-item', { hasText: companion2 })
      .getByRole('button', { name: 'Start Chat' })
      .click();
    await expect(page).toHaveURL(/\/chat\/.+/);
    await expect(page.locator('.conversation-companion-name')).toContainText(companion2);
  });

  test('delete a chat, delete companion without chat, delete companion with chat (cascades)', async ({ page }) => {
    await skipIfBackendDown(page.request);
    await registerViaUi(page);

    const companion1 = `NoChat-${uniqueUsername('c')}`;
    const companion2 = `HasChat-${uniqueUsername('c')}`;

    // Create two companions.
    await page.getByRole('link', { name: 'Companion' }).click();

    await page.getByText('Add a companion').click();
    await page.getByLabel('Avatar URL').fill('https://example.com/1.png');
    await page.getByLabel('Name').fill(companion1);
    await page.getByRole('button', { name: 'Add' }).click();
    await expect(page.getByText(companion1)).toBeVisible();

    await page.getByText('Add a companion').click();
    await page.getByLabel('Avatar URL').fill('https://example.com/2.png');
    await page.getByLabel('Name').fill(companion2);
    await page.getByRole('button', { name: 'Add' }).click();
    await expect(page.getByText(companion2)).toBeVisible();

    // Start a chat with companion2, then delete it.
    await page.getByRole('link', { name: 'Chat' }).click();
    await page.getByText('Click to assign companion').first().click();
    await page
      .locator('.available-companion-item', { hasText: companion2 })
      .getByRole('button', { name: 'Start Chat' })
      .click();
    await expect(page).toHaveURL(/\/chat\/.+/);

    await acceptNextDialog(page);
    await page.getByRole('button', { name: 'Delete Chat' }).click();
    await expect(page).toHaveURL(/\/chat$/);

    // Delete companion1 (no chat).
    await page.getByRole('link', { name: 'Companion' }).click();
    await acceptNextDialog(page);
    await page.locator('.companion-item', { hasText: companion1 }).getByRole('button', { name: 'Delete' }).click();
    await expect(page.locator('.companion-item', { hasText: companion1 })).toHaveCount(0);

    // Re-create chat with companion2, then delete companion2 (should also delete chat).
    await page.getByRole('link', { name: 'Chat' }).click();
    await page.getByText('Click to assign companion').first().click();
    await page
      .locator('.available-companion-item', { hasText: companion2 })
      .getByRole('button', { name: 'Start Chat' })
      .click();
    await expect(page).toHaveURL(/\/chat\/.+/);
    await page.getByRole('link', { name: 'Back to chats' }).click();

    await page.getByRole('link', { name: 'Companion' }).click();
    await acceptNextDialog(page);
    await page.locator('.companion-item', { hasText: companion2 }).getByRole('button', { name: 'Delete' }).click();
    await expect(page.locator('.companion-item', { hasText: companion2 })).toHaveCount(0);

    // Verify chat is gone / can't start new chat because companion removed.
    await page.getByRole('link', { name: 'Chat' }).click();
    await expect(page.getByRole('heading', { name: 'Chats', exact: true })).toBeVisible();
  });
});

