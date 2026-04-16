import { expect } from '@playwright/test';

export function uniqueUsername(prefix = 'navi') {
  // Must match frontend USER_REGEX: starts with letter, 4-24 chars, [a-zA-Z0-9-_]
  const stamp = Date.now().toString(36);
  const rand = Math.random().toString(36).slice(2, 6);
  return `${prefix}${stamp}${rand}`.slice(0, 24);
}

export const VALID_PASSWORD = 'NaviTest1!';

export async function backendIsReachable(request) {
  try {
    const res = await request.get('http://127.0.0.1:8000/', { timeout: 2000 });
    return !!res;
  } catch {
    return false;
  }
}

export async function registerViaUi(page, { username, password = VALID_PASSWORD } = {}) {
  const user = username ?? uniqueUsername('navitest');

  await page.goto('/register');
  await page.getByLabel('Username').fill(user);
  await page.getByLabel('Password', { exact: true }).fill(password);
  await page.getByLabel('Confirm password').fill(password);

  const submit = page.getByRole('button', { name: 'Sign Up' });
  await expect(submit).toBeEnabled();
  await submit.click();

  const errorMessage = page.locator('.error-message');
  const navigated = page.waitForURL(/\/chat$/, { timeout: 15000 }).then(() => true).catch(() => false);
  const errored = errorMessage.waitFor({ state: 'visible', timeout: 15000 }).then(() => true).catch(() => false);

  const [didNavigate, didError] = await Promise.all([navigated, errored]);

  if (!didNavigate) {
    const msg = didError ? await errorMessage.innerText().catch(() => '') : '';
    throw new Error(
      `Registration did not redirect to /chat. ${didError ? `UI error: "${msg}"` : 'No UI error message found.'}`
    );
  }

  await expect(page.getByRole('heading', { name: 'Chats', exact: true })).toBeVisible({ timeout: 15000 });

  return { username: user, password };
}

export async function loginViaUi(page, { username, password, rememberMe } = {}) {
  await page.goto('/login');

  const remember = page.locator('#remember-me');
  if (typeof rememberMe === 'boolean') {
    if (rememberMe) await remember.check();
    else await remember.uncheck();
  }

  await page.getByLabel('Username').fill(username ?? '');
  await page.getByLabel('Password', { exact: true }).fill(password ?? '');
  await page.getByRole('button', { name: 'Sign In' }).click();
}

export async function clearSession(page) {
  await page.context().clearCookies();
  await page.goto('/login');
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });
  await page.reload();
}

export async function acceptNextDialog(page) {
  page.once('dialog', async (dialog) => {
    await dialog.accept();
  });
}

