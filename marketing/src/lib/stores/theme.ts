/**
 * Foldline Design System - Theme Store
 * Light/Dark mode management with localStorage persistence
 */

import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type Theme = 'light' | 'dark';

// Initialize theme from localStorage or system preference
function getInitialTheme(): Theme {
  if (!browser) return 'light';

  // Check localStorage first
  const stored = localStorage.getItem('foldline-theme');
  if (stored === 'light' || stored === 'dark') {
    return stored as Theme;
  }

  // Fall back to system preference
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'dark';
  }

  return 'light';
}

// Create the writable store
function createThemeStore() {
  const { subscribe, set, update } = writable<Theme>(getInitialTheme());

  return {
    subscribe,
    set: (value: Theme) => {
      if (browser) {
        localStorage.setItem('foldline-theme', value);
        document.documentElement.classList.remove('light', 'dark');
        document.documentElement.classList.add(value);
      }
      set(value);
    },
    toggle: () => {
      update((current) => {
        const newTheme = current === 'light' ? 'dark' : 'light';
        if (browser) {
          localStorage.setItem('foldline-theme', newTheme);
          document.documentElement.classList.remove('light', 'dark');
          document.documentElement.classList.add(newTheme);
        }
        return newTheme;
      });
    },
    initialize: () => {
      if (browser) {
        const theme = getInitialTheme();
        document.documentElement.classList.add(theme);
        set(theme);
      }
    }
  };
}

export const theme = createThemeStore();
