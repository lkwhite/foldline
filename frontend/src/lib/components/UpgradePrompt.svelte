<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { PremiumFeature } from '$lib/stores/license';

  export let feature: PremiumFeature;
  export let inline: boolean = false; // inline vs modal display

  const dispatch = createEventDispatcher();

  const featureDescriptions: Record<PremiumFeature, { title: string; description: string }> = {
    unlimited_import: {
      title: 'Unlimited Data Sources',
      description: 'Import from all supported devices and platforms, not just Garmin.'
    },
    full_history: {
      title: 'Full Historical Data',
      description: 'Access your complete data history, not just the last 30 days.'
    },
    correlation_analysis: {
      title: 'Correlation Analysis',
      description: 'Discover relationships between different metrics with advanced correlation tools.'
    },
    data_export: {
      title: 'Data Export',
      description: 'Export your data to CSV, JSON, or FIT formats for use in other tools.'
    },
    advanced_filters: {
      title: 'Advanced Filters',
      description: 'Create complex queries and filters to analyze specific data patterns.'
    },
    custom_date_ranges: {
      title: 'Custom Date Ranges',
      description: 'Select any date range for analysis, not just predefined periods.'
    },
    multi_metric_heatmaps: {
      title: 'Multi-Metric Heatmaps',
      description: 'Compare multiple metrics simultaneously in calendar heatmaps.'
    }
  };

  const info = featureDescriptions[feature];

  function handleUpgrade() {
    dispatch('upgrade');
  }
</script>

{#if inline}
  <!-- Inline upgrade prompt (for feature gates) -->
  <div class="upgrade-inline">
    <div class="upgrade-icon">🔒</div>
    <div class="upgrade-content">
      <h3 class="upgrade-title">{info.title}</h3>
      <p class="upgrade-description">{info.description}</p>
      <div class="upgrade-actions">
        <a href="/buy" class="btn btn-cta btn-small">Upgrade to Premium</a>
        <button class="btn btn-secondary btn-small" on:click={handleUpgrade}>
          I have a license key
        </button>
      </div>
    </div>
  </div>
{:else}
  <!-- Banner upgrade prompt (for in-page promotions) -->
  <div class="upgrade-banner">
    <div class="banner-content">
      <div class="banner-icon">🔒</div>
      <div class="banner-text">
        <strong>{info.title}</strong> is a premium feature.
        <span class="banner-subtext">{info.description}</span>
      </div>
    </div>
    <div class="banner-actions">
      <a href="/buy" class="btn btn-cta btn-small">Upgrade</a>
    </div>
  </div>
{/if}

<style>
  /* Inline upgrade prompt */
  .upgrade-inline {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-xxl);
    text-align: center;
    background-color: var(--color-bg);
    border: var(--stroke-weight) solid var(--line-color);
    border-radius: var(--border-radius-medium);
    min-height: 300px;
  }

  .upgrade-icon {
    font-size: 48px;
    margin-bottom: var(--space-l);
    opacity: 0.5;
  }

  .upgrade-content {
    max-width: 480px;
  }

  .upgrade-title {
    font-size: var(--type-h3);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin-bottom: var(--space-s);
  }

  .upgrade-description {
    font-size: var(--type-body);
    line-height: var(--line-height-normal);
    color: var(--color-text-secondary);
    margin-bottom: var(--space-xl);
  }

  .upgrade-actions {
    display: flex;
    flex-direction: column;
    gap: var(--space-m);
    align-items: center;
  }

  .upgrade-actions .btn {
    min-width: 200px;
  }

  /* Banner upgrade prompt */
  .upgrade-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-m) var(--space-l);
    background-color: rgba(230, 159, 0, 0.1);
    border: var(--stroke-weight) solid var(--color-accent);
    border-radius: var(--border-radius-medium);
    margin-bottom: var(--space-l);
    gap: var(--space-l);
  }

  .banner-content {
    display: flex;
    align-items: center;
    gap: var(--space-m);
    flex: 1;
  }

  .banner-icon {
    font-size: 24px;
    flex-shrink: 0;
  }

  .banner-text {
    font-size: var(--type-body-small);
    line-height: var(--line-height-normal);
    color: var(--color-text);
  }

  .banner-text strong {
    color: var(--color-accent);
    font-weight: var(--font-weight-medium);
  }

  .banner-subtext {
    display: block;
    color: var(--color-text-secondary);
    margin-top: 2px;
  }

  .banner-actions {
    flex-shrink: 0;
  }

  /* Button variants */
  .btn-small {
    padding: 8px 16px;
    font-size: var(--type-body-small);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .upgrade-inline {
      padding: var(--space-xl);
      min-height: 250px;
    }

    .upgrade-icon {
      font-size: 36px;
    }

    .upgrade-title {
      font-size: var(--type-body);
    }

    .upgrade-description {
      font-size: var(--type-body-small);
    }

    .upgrade-banner {
      flex-direction: column;
      align-items: flex-start;
      gap: var(--space-m);
    }

    .banner-actions {
      width: 100%;
    }

    .banner-actions .btn {
      width: 100%;
    }
  }
</style>
