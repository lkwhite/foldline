<script lang="ts">
  import { theme } from '$lib/stores/theme';

  export let title: string = 'Your physiological map, unfolded.';
  export let subtitle: string = 'Foldline maps your wearable data the way topographic maps reveal terrain: clean, structured, understated, and precise.';
  export let ctaPrimary: string = 'Download for macOS';
  export let ctaSecondary: string = 'Learn More';
  export let screenshotSrc: string = '/screenshots/hero-screenshot.png';
  export let screenshotAlt: string = 'Foldline dashboard screenshot';
</script>

<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <!-- Left: Text Content -->
      <div class="hero-content">
        <!-- Small logo -->
        <div class="hero-logo">
          <img
            src={$theme === 'dark' ? '/brand/logo-dark.svg' : '/brand/logo-light.svg'}
            alt="Foldline logo"
            width="40"
            height="120"
          />
        </div>

        <h1 class="hero-title">{title}</h1>

        <p class="hero-subtitle">{subtitle}</p>

        <div class="hero-ctas">
          <button class="btn btn-cta">{ctaPrimary}</button>
          <button class="btn btn-secondary">{ctaSecondary}</button>
        </div>
      </div>

      <!-- Right: Screenshot -->
      <div class="hero-screenshot">
        <div class="screenshot-container">
          <img
            src={screenshotSrc}
            alt={screenshotAlt}
            loading="eager"
          />
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .hero {
    padding: calc(var(--space-xxl) * 2) 0;
    min-height: 80vh;
    display: flex;
    align-items: center;
  }

  .hero-grid {
    display: grid;
    grid-template-columns: 40% 60%;
    gap: var(--space-xxl);
    align-items: center;
  }

  .hero-content {
    display: flex;
    flex-direction: column;
    gap: var(--space-l);
  }

  .hero-logo {
    margin-bottom: var(--space-s);
  }

  .hero-title {
    font-size: var(--type-h1);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-tight);
    color: var(--color-text);
  }

  .hero-subtitle {
    font-size: var(--type-h3);
    line-height: var(--line-height-normal);
    color: var(--color-text-secondary);
    max-width: 540px;
  }

  .hero-ctas {
    display: flex;
    gap: var(--space-m);
    margin-top: var(--space-m);
  }

  .hero-screenshot {
    position: relative;
  }

  .hero-screenshot .screenshot-container {
    border-radius: var(--border-radius-small);
    overflow: hidden;
  }

  .hero-screenshot img {
    width: 100%;
    height: auto;
    display: block;
  }

  /* Responsive: Mobile stacking */
  @media (max-width: 1024px) {
    .hero {
      min-height: auto;
      padding: var(--space-xxl) 0;
    }

    .hero-grid {
      grid-template-columns: 1fr;
      gap: var(--space-xxl);
    }

    .hero-screenshot {
      order: 2;
    }

    .hero-content {
      order: 1;
    }

    .hero-subtitle {
      max-width: 100%;
    }
  }

  @media (max-width: 768px) {
    .hero-ctas {
      flex-direction: column;
      width: 100%;
    }

    .hero-ctas .btn {
      width: 100%;
    }

    .hero-logo img {
      width: 30px;
      height: 90px;
    }
  }
</style>
