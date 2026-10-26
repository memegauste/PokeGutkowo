import { StrictMode } from 'react';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import App from './App.jsx';

const posts = [1, 2, 3].map((id) => ({
  id, title: `Post ${id}`, context: `<p>Treść ${id}</p>`, author: 'Trener',
}));

function mockApi(overrides = {}) {
  const data = { '/settings/': {}, '/posts/': posts, '/players/': [], ...overrides };
  vi.stubGlobal('fetch', vi.fn(async (path) => ({
    ok: true,
    json: async () => data[path],
  })));
}

beforeEach(() => {
  window.history.replaceState({}, '', '/');
  mockApi();
});

afterEach(() => vi.unstubAllGlobals());

test('renders posts and changes pages with accessible buttons', async () => {
  const user = userEvent.setup();
  render(<App />);
  expect(await screen.findByRole('heading', { name: 'Post 1' })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Post 2' })).toBeInTheDocument();
  expect(screen.queryByRole('heading', { name: 'Post 3' })).not.toBeInTheDocument();
  await user.click(screen.getByRole('button', { name: '2' }));
  expect(screen.getByRole('heading', { name: 'Post 3' })).toBeInTheDocument();
  expect(screen.queryByRole('heading', { name: 'Post 1' })).not.toBeInTheDocument();
});

test('navigates to players with React Router and renders trainer data', async () => {
  mockApi({ '/players/': [{ id: 1, nickname: 'Pikachu', level: 40, team: 'mystic', trainer_code: '123456789012' }] });
  const user = userEvent.setup();
  render(<App />);
  await user.click(screen.getByRole('link', { name: 'Gracze' }));
  expect(await screen.findByRole('heading', { name: 'Pikachu' })).toBeInTheDocument();
  expect(screen.getByText('Kod trenera: 123456789012')).toBeInTheDocument();
  expect(window.location.pathname).toBe('/players');
  expect(screen.getByRole('link', { name: 'Gracze' })).toHaveAttribute('aria-current', 'page');
});

test('shows settings, links, and screenshot on a direct visit to about', async () => {
  window.history.replaceState({}, '', '/aboutme');
  mockApi({ '/settings/': { title: 'Trenerzy Gutkowa', owner_about: 'Cześć!', discord: 'https://discord.gg/example', owner_screenshot: '/media/trainer.png' } });
  render(<App />);
  expect(await screen.findByText('Cześć!')).toBeInTheDocument();
  expect(screen.getByRole('link', { name: 'Trenerzy Gutkowa' })).toBeInTheDocument();
  expect(screen.getByRole('link', { name: 'Discord' })).toHaveAttribute('href', 'https://discord.gg/example');
  expect(screen.getByRole('img')).toHaveAttribute('src', '/media/trainer.png');
});

test('handles an empty database without broken images or links', async () => {
  mockApi({ '/posts/': [] });
  const user = userEvent.setup();
  render(<App />);
  expect(await screen.findByText('Nie ma jeszcze postów.')).toBeInTheDocument();
  await user.click(screen.getByRole('link', { name: 'O mnie' }));
  expect(await screen.findByText('Właściciel nie dodał jeszcze opisu.')).toBeInTheDocument();
  expect(screen.queryByRole('img')).not.toBeInTheDocument();
  expect(screen.queryByRole('link', { name: 'Discord' })).not.toBeInTheDocument();
});

test.each(['network', 'http', 'json', 'shape'])('ends the loading state after an API %s error', async (failure) => {
  vi.stubGlobal('fetch', vi.fn(async (path) => {
    if (path === '/settings/') return { ok: true, json: async () => ({}) };
    if (failure === 'network') throw new Error('Offline');
    return {
      ok: failure !== 'http',
      json: async () => {
        if (failure === 'json') throw new SyntaxError('Invalid JSON');
        return { detail: 'Unexpected response' };
      },
    };
  }));
  render(<App />);
  expect(await screen.findByRole('alert')).toHaveTextContent('Nie udało się pobrać danych.');
  expect(screen.queryByRole('status')).not.toBeInTheDocument();
});

test('sanitizes HTML from posts while keeping formatting', async () => {
  mockApi({ '/posts/': [{ id: 1, title: 'Bezpieczny post', author: 'Trener', context: '<p><strong>Witaj</strong></p><img src="x" onerror="alert(1)"><script>alert(1)</script><a href="javascript:alert(1)">Link</a>' }] });
  render(<App />);
  const article = (await screen.findByRole('heading', { name: 'Bezpieczny post' })).closest('article');
  expect(within(article).getByText('Witaj').tagName).toBe('STRONG');
  expect(article.querySelector('script')).toBeNull();
  expect(article.querySelector('img')).not.toHaveAttribute('onerror');
  expect(within(article).getByText('Link')).not.toHaveAttribute('href');
});

test('loads successfully in React StrictMode after effect cleanup', async () => {
  render(<StrictMode><App /></StrictMode>);
  expect(await screen.findByRole('heading', { name: 'Post 1' })).toBeInTheDocument();
});

test('renders a missing-page message for unknown routes', async () => {
  window.history.replaceState({}, '', '/missing');
  render(<App />);
  expect(await screen.findByRole('heading', { name: 'Nie znaleziono strony.' })).toBeInTheDocument();
});
