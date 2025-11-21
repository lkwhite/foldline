<script lang="ts">
  import HeroSection from '$lib/components/marketing/HeroSection.svelte';
  import FeatureBlock from '$lib/components/marketing/FeatureBlock.svelte';
  import ScreenshotShowcase from '$lib/components/marketing/ScreenshotShowcase.svelte';
  import Footer from '$lib/components/marketing/Footer.svelte';

  const screenshots = [
    {
      src: '/screenshots/hero-dashboard.svg',
      alt: 'Foldline dashboard overview',
      caption: 'Interactive dashboard with your complete physiological timeline'
    },
    {
      src: '/screenshots/feature-heatmaps.svg',
      alt: 'Calendar heatmap view',
      caption: 'Spot patterns across weeks, months, and years at a glance'
    },
    {
      src: '/screenshots/feature-trends.svg',
      alt: 'Multi-metric trend analysis',
      caption: 'Correlate metrics to discover what actually affects your performance'
    }
  ];
</script>

<svelte:head>
  <title>Foldline - Your physiological map, unfolded</title>
  <meta name="description" content="Privacy-first wearable data analyzer. Map your physiological data the way topographic maps reveal terrain: clean, structured, understated, and precise." />
</svelte:head>

<!-- Hero Section -->
<HeroSection
  title="Your physiological map, unfolded."
  subtitle="Foldline maps your wearable data the way topographic maps reveal terrain: clean, structured, understated, and precise."
  ctaPrimary="Download for macOS"
  ctaSecondary="View Documentation"
  screenshotSrc="/screenshots/hero-dashboard.svg"
  screenshotAlt="Foldline dashboard showcasing clean data visualization"
/>

<!-- Feature Blocks -->
<section class="features">
  <FeatureBlock
    title="Heatmaps that reveal patterns"
    description="See your entire activity history at once. Calendar heatmaps make it easy to spot weekly rhythms, seasonal trends, and outliers across months of data."
    screenshotSrc="/screenshots/feature-heatmaps.svg"
    screenshotAlt="Calendar heatmap showing activity patterns over time"
    reverse={false}
  />

  <FeatureBlock
    title="Trends without the noise"
    description="Track multiple metrics over time with clean, minimal line charts. Filter by date range, compare periods, and export your insights."
    screenshotSrc="/screenshots/feature-trends.svg"
    screenshotAlt="Trend analysis showing metric correlations"
    reverse={true}
  />

  <FeatureBlock
    title="Privacy-first, local-only"
    description="All your wearable data stays on your machine. No cloud uploads, no tracking, no external API calls. Just you and your data."
    screenshotSrc="/screenshots/hero-dashboard.svg"
    screenshotAlt="Local data processing interface"
    reverse={false}
  />
</section>

<!-- Screenshot Showcase -->
<ScreenshotShowcase
  title="See your data, unfolded"
  {screenshots}
/>

<!-- Footer -->
<Footer />

<style>
  .features {
    background-color: var(--color-bg);
  }

  /* Add subtle map outline motif behind features section */
  .features::before {
    content: '';
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 300px;
    height: 900px;
    border: var(--stroke-weight) solid var(--line-color);
    border-radius: var(--border-radius-small);
    opacity: 0.1;
    pointer-events: none;
    z-index: 0;
  }

  .features {
    position: relative;
  }
</style>
