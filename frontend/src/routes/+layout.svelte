<script lang="ts">
  import '../app.css';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { theme } from '$lib/stores/theme';
  import ThemeToggle from '$lib/components/marketing/ThemeToggle.svelte';

  // Initialize theme on mount
  onMount(() => {
    theme.initialize();
  });
</script>

<div class="app">
  <nav class="nav">
    <div class="nav-content">
      <!-- Logo -->
      <a href="/" class="logo-link">
        <img
          src={$theme === 'dark' ? '/brand/logo-dark.svg' : '/brand/logo-light.svg'}
          alt="Foldline"
          class="logo-img"
          width="30"
          height="75"
        />
      </a>

      <!-- Navigation Links -->
      <div class="nav-links">
        <a href="/marketing" class="nav-link" class:active={$page.url.pathname === '/marketing'}>Marketing</a>
        <a href="/" class="nav-link" class:active={$page.url.pathname === '/'}>Setup</a>
        <a href="/dashboard" class="nav-link" class:active={$page.url.pathname === '/dashboard'}>Dashboard</a>
        <a href="/heatmaps" class="nav-link" class:active={$page.url.pathname === '/heatmaps'}>Heatmaps</a>
        <a href="/trends" class="nav-link" class:active={$page.url.pathname === '/trends'}>Trends</a>
        <a href="/correlation" class="nav-link" class:active={$page.url.pathname === '/correlation'}>Correlation</a>
        <a href="/settings" class="nav-link" class:active={$page.url.pathname === '/settings'}>Settings</a>
        <a href="/about" class="nav-link" class:active={$page.url.pathname === '/about'}>About</a>
      </div>

      <!-- Theme Toggle -->
      <ThemeToggle />
    </div>
  </nav>

  <main>
    <slot />
  </main>
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .nav {
    background-color: transparent;
    border-bottom: var(--stroke-weight) solid var(--line-color);
    padding: 0 var(--space-xl);
    position: sticky;
    top: 0;
    z-index: var(--z-nav);
    backdrop-filter: blur(8px);
    background-color: rgba(var(--color-bg), 0.8);
  }

  .nav-content {
    max-width: var(--container-max-width);
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: var(--nav-height);
    gap: var(--space-l);
  }

  .logo-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    flex-shrink: 0;
  }

  .logo-img {
    display: block;
    width: 30px;
    height: 75px;
  }

  .nav-links {
    display: flex;
    gap: var(--space-l);
    flex: 1;
    justify-content: center;
  }

  .nav-link {
    color: var(--color-text-secondary);
    text-decoration: none;
    font-size: var(--type-body-small);
    font-weight: var(--font-weight-regular);
    transition: color var(--transition-duration) var(--transition-easing);
    position: relative;
    padding: 4px 0;
  }

  .nav-link:hover {
    color: var(--color-text);
  }

  .nav-link.active {
    color: var(--color-accent);
  }

  /* Minimal underline for active link */
  .nav-link.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: var(--stroke-weight);
    background-color: var(--color-accent);
  }

  main {
    flex: 1;
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .nav {
      padding: 0 var(--space-m);
    }

    .nav-links {
      gap: var(--space-m);
      font-size: var(--type-micro);
    }
  }

  @media (max-width: 768px) {
    .nav-content {
      height: 56px;
    }

    .logo-img {
      width: 25px;
      height: 63px;
    }

    .nav-links {
      display: none; /* Hide nav links on mobile - could be replaced with hamburger menu */
    }
  }
</style>
