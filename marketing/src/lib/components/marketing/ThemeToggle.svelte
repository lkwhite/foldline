<script lang="ts">
  import { theme } from '$lib/stores/theme';

  function toggleTheme() {
    theme.toggle();
  }
</script>

<button
  class="theme-toggle"
  on:click={toggleTheme}
  aria-label="Toggle theme"
  title={$theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
>
  {#if $theme === 'light'}
    <!-- Moon icon for dark mode -->
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M17 10.5C16.9 14.64 13.64 18 9.5 18C5.36 18 2 14.64 2 10.5C2 6.36 5.36 3 9.5 3C9.67 3 9.83 3.01 10 3.03C8.84 4.24 8.5 6.27 9.24 7.96C10.13 10 12.5 11.5 14.96 11.24C16.41 11.08 17.62 10.5 17 10.5Z"
        stroke="currentColor"
        stroke-width="1.25"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  {:else}
    <!-- Sun icon for light mode -->
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle
        cx="10"
        cy="10"
        r="3.5"
        stroke="currentColor"
        stroke-width="1.25"
      />
      <line x1="10" y1="2" x2="10" y2="4" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
      <line x1="10" y1="16" x2="10" y2="18" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
      <line x1="18" y1="10" x2="16" y2="10" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
      <line x1="4" y1="10" x2="2" y2="10" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
      <line x1="15.536" y1="4.464" x2="14.121" y2="5.879" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
      <line x1="5.879" y1="14.121" x2="4.464" y2="15.536" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
      <line x1="15.536" y1="15.536" x2="14.121" y2="14.121" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
      <line x1="5.879" y1="5.879" x2="4.464" y2="4.464" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" />
    </svg>
  {/if}
</button>

<style>
  .theme-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    padding: 0;
    background: transparent;
    border: var(--stroke-weight) solid var(--line-color);
    border-radius: var(--border-radius-medium);
    color: var(--color-text);
    cursor: pointer;
    transition:
      border-color var(--transition-duration) var(--transition-easing),
      color var(--transition-duration) var(--transition-easing),
      transform var(--transition-duration) var(--transition-easing);
  }

  .theme-toggle:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
    transform: translateY(-1px);
  }

  .theme-toggle:active {
    transform: translateY(0);
  }

  svg {
    display: block;
  }
</style>
