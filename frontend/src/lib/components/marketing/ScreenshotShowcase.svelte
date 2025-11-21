<script lang="ts">
  export let title: string = 'See your data, unfolded';
  export let screenshots: Array<{
    src: string;
    alt: string;
    caption?: string;
  }> = [];
</script>

<section class="showcase">
  <div class="container">
    {#if title}
      <h2 class="showcase-title">{title}</h2>
    {/if}

    <div class="showcase-grid">
      {#each screenshots as screenshot, i}
        <div class="showcase-item">
          <div class="screenshot-container brightness-hover">
            <img
              src={screenshot.src}
              alt={screenshot.alt}
              loading="lazy"
            />
          </div>
          {#if screenshot.caption}
            <p class="screenshot-caption">{screenshot.caption}</p>
          {/if}
        </div>

        {#if i < screenshots.length - 1}
          <hr class="separator-horizontal separator-thin" />
        {/if}
      {/each}
    </div>
  </div>
</section>

<style>
  .showcase {
    padding: calc(var(--space-xxl) * 2) 0;
  }

  .showcase-title {
    font-size: var(--type-h2);
    font-weight: var(--font-weight-medium);
    text-align: center;
    margin-bottom: calc(var(--space-xxl) * 1.5);
    color: var(--color-text);
  }

  .showcase-grid {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .showcase-item {
    display: flex;
    flex-direction: column;
    gap: var(--space-m);
  }

  .showcase-item .screenshot-container {
    max-width: 900px;
    margin: 0 auto;
    width: 100%;
    border-radius: var(--border-radius-small);
    overflow: hidden;
  }

  .showcase-item img {
    width: 100%;
    height: auto;
    display: block;
  }

  .screenshot-caption {
    text-align: center;
    font-size: var(--type-body-small);
    color: var(--color-text-secondary);
    margin-top: var(--space-s);
  }

  /* Separator between screenshots */
  .separator-horizontal {
    margin: var(--space-xxl) 0;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .showcase {
      padding: var(--space-xxl) 0;
    }

    .showcase-title {
      margin-bottom: var(--space-xxl);
    }

    .separator-horizontal {
      margin: var(--space-l) 0;
    }
  }
</style>
