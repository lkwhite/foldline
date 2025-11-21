<script lang="ts">
  export let title: string;
  export let description: string;
  export let screenshotSrc: string;
  export let screenshotAlt: string;
  export let reverse: boolean = false;
</script>

<div class="feature-block" class:reverse>
  <div class="container">
    <div class="feature-grid">
      <!-- Text Content -->
      <div class="feature-content">
        <h2 class="feature-title">{title}</h2>
        <p class="feature-description">{description}</p>
      </div>

      <!-- Screenshot -->
      <div class="feature-screenshot">
        <div class="screenshot-container brightness-hover">
          <img
            src={screenshotSrc}
            alt={screenshotAlt}
            loading="lazy"
          />
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .feature-block {
    padding: var(--space-xxl) 0;
    border-top: var(--stroke-weight) solid var(--line-color);
  }

  .feature-grid {
    display: grid;
    grid-template-columns: 40% 60%;
    gap: var(--space-xxl);
    align-items: center;
  }

  /* Reverse layout (screenshot on left) */
  .feature-block.reverse .feature-grid {
    grid-template-columns: 60% 40%;
  }

  .feature-block.reverse .feature-content {
    order: 2;
  }

  .feature-block.reverse .feature-screenshot {
    order: 1;
  }

  .feature-content {
    display: flex;
    flex-direction: column;
    gap: var(--space-m);
  }

  .feature-title {
    font-size: var(--type-h2);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-tight);
    color: var(--color-text);
  }

  .feature-description {
    font-size: var(--type-body);
    line-height: var(--line-height-relaxed);
    color: var(--color-text-secondary);
    max-width: 540px;
  }

  .feature-screenshot {
    position: relative;
  }

  .feature-screenshot .screenshot-container {
    border-radius: var(--border-radius-small);
    overflow: hidden;
  }

  .feature-screenshot img {
    width: 100%;
    height: auto;
    display: block;
  }

  /* Responsive: Mobile stacking */
  @media (max-width: 1024px) {
    .feature-grid {
      grid-template-columns: 1fr !important;
      gap: var(--space-l);
    }

    .feature-block.reverse .feature-content {
      order: 1;
    }

    .feature-block.reverse .feature-screenshot {
      order: 2;
    }

    .feature-description {
      max-width: 100%;
    }
  }

  @media (max-width: 768px) {
    .feature-block {
      padding: var(--space-l) 0;
    }
  }
</style>
