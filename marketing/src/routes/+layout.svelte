<script lang="ts">
  import '../app.css';
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

  main {
    flex: 1;
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .nav {
      padding: 0 var(--space-m);
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
  }
</style>
