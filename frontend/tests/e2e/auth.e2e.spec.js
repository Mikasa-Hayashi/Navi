import { expect, test } from '@playwright/test';
import { backendIsReachable, clearSession, loginViaUi, registerViaUi, uniqueUsername, VALID_PASSWORD } from './_helpers.js';

test.describe.serial('Auth (register/login/remember me) + edge/security cases', () => {
  async function skipIfBackendDown(request) {
    const ok = await backendIsReachable(request);
    test.skip(!ok, 'Backend not reachable on http://127.0.0.1:8000 (start backend before running e2e)');
  }

  test('registration: invalid inputs keep submit disabled (regex + edge cases)', async ({ page }) => {
    await page.goto('/register');

    const username = page.getByLabel('Username');
    const password = page.getByLabel('Password', { exact: true });
    const confirm = page.getByLabel('Confirm password');
    const submit = page.getByRole('button', { name: 'Sign Up' });

    // Empty
    await expect(submit).toBeDisabled();

    // Single character username (too short)
    await username.fill('a');
    await password.fill(VALID_PASSWORD);
    await confirm.fill(VALID_PASSWORD);
    await expect(submit).toBeDisabled();

    // Long username (too long)
    await username.fill('a'.repeat(40));
    await expect(submit).toBeDisabled();

    // Special chars / XSS payload
    await username.fill('<script>alert(1)</script>');
    await expect(submit).toBeDisabled();

    // SQLi-like payload
    await username.fill("a' OR 1=1--");
    await expect(submit).toBeDisabled();

    // Valid username but invalid password (missing required special char)
    await username.fill(uniqueUsername('navireg'));
    await password.fill('NoSpecial1A');
    await confirm.fill('NoSpecial1A');
    await expect(submit).toBeDisabled();

    // Valid password but mismatch confirm
    await password.fill(VALID_PASSWORD);
    await confirm.fill(`${VALID_PASSWORD}x`);
    await expect(submit).toBeDisabled();
  });

  test('registration: valid data succeeds and redirects to chat', async ({ page }) => {
    await skipIfBackendDown(page.request);
    await registerViaUi(page);
  });

  test('login: incorrect data shows error and stays on login', async ({ page }) => {
    await skipIfBackendDown(page.request);
    await page.goto('/login');
    await page.getByLabel('Username').fill('doesnotexistuser');
    await page.getByLabel('Password', { exact: true }).fill('WrongPass1!');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page).toHaveURL(/\/login$/);
    await expect(page.locator('.error-message')).toContainText(/Unauthorized|Login Failed/i);
  });

  test('login: SQLi/XSS payloads do not bypass auth and do not execute', async ({ page }) => {
    await skipIfBackendDown(page.request);
    let sawAlert = false;
    page.on('dialog', (dialog) => {
      if (dialog.type() === 'alert') sawAlert = true;
      dialog.dismiss().catch(() => {});
    });

    await page.goto('/login');
    await page.getByLabel('Username').fill("admin' OR '1'='1");
    await page.getByLabel('Password', { exact: true }).fill("anything' OR '1'='1");
    await page.getByRole('button', { name: 'Sign In' }).click();
    await expect(page).toHaveURL(/\/login$/);

    await page.getByLabel('Username').fill('<img src=x onerror=alert(1)>');
    await page.getByLabel('Password', { exact: true }).fill('<script>alert(1)</script>');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await expect(page).toHaveURL(/\/login$/);

    expect(sawAlert).toBe(false);
  });

  test('login: must create account by registering, then successful login redirects to chat', async ({ page }) => {
    await skipIfBackendDown(page.request);
    const creds = await registerViaUi(page);

    await clearSession(page);
    await loginViaUi(page, { ...creds, rememberMe: false });

    await expect(page).toHaveURL(/\/chat$/);
    await expect(page.getByRole('heading', { name: 'Chats', exact: true })).toBeVisible();
  });

  test('Remember me: checked survives refresh; unchecked redirects back to login after refresh', async ({ page }) => {
    await skipIfBackendDown(page.request);
    const creds = await registerViaUi(page);

    // Checked: should restore via refresh token after reload.
    await clearSession(page);
    await loginViaUi(page, { ...creds, rememberMe: true });
    await expect(page).toHaveURL(/\/chat$/);
    await page.reload();
    await expect(page).toHaveURL(/\/chat$/);

    // Unchecked: should not restore after reload.
    await clearSession(page);
    await loginViaUi(page, { ...creds, rememberMe: false });
    await expect(page).toHaveURL(/\/chat$/);
    await page.reload();
    await expect(page).toHaveURL(/\/login$/);
    await expect(page.getByLabel('Username')).toHaveValue('');
    await expect(page.getByLabel('Password', { exact: true })).toHaveValue('');
  });
});

