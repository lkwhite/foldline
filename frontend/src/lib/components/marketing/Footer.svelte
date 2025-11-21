<script lang="ts">
  import { theme } from '$lib/stores/theme';

  const currentYear = new Date().getFullYear();

  export let links = [
    { label: 'Download', href: '#download' },
    { label: 'Features', href: '#features' },
    { label: 'Documentation', href: '#docs' },
    { label: 'Privacy', href: '#privacy' }
  ];

  export let socialLinks = [
    { label: 'GitHub', href: 'https://github.com/yourusername/foldline' },
    { label: 'Twitter', href: '#' }
  ];
</script>

<footer class="footer fold-line-bg">
  <div class="container">
    <div class="footer-grid">
      <!-- Logo & Tagline -->
      <div class="footer-brand">
        <div class="footer-logo">
          <img
            src={$theme === 'dark' ? '/brand/logo-dark.svg' : '/brand/logo-light.svg'}
            alt="Foldline logo"
            width="40"
            height="100"
          />
        </div>
        <p class="footer-tagline">Your physiological map, unfolded.</p>
      </div>

      <!-- Navigation Links -->
      <div class="footer-links">
        <h3 class="footer-heading">Links</h3>
        <nav>
          <ul>
            {#each links as link}
              <li>
                <a href={link.href} class="footer-link">{link.label}</a>
              </li>
            {/each}
          </ul>
        </nav>
      </div>

      <!-- Social Links -->
      <div class="footer-social">
        <h3 class="footer-heading">Connect</h3>
        <nav>
          <ul>
            {#each socialLinks as social}
              <li>
                <a
                  href={social.href}
                  class="footer-link"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {social.label}
                </a>
              </li>
            {/each}
          </ul>
        </nav>
      </div>
    </div>

    <!-- Copyright -->
    <div class="footer-copyright">
      <p>© {currentYear} Foldline. Privacy-first wearable data analyzer.</p>
    </div>
  </div>
</footer>

<style>
  .footer {
    border-top: var(--stroke-weight) solid var(--line-color);
    padding: var(--space-xxl) 0 var(--space-l) 0;
    margin-top: calc(var(--space-xxl) * 2);
    position: relative;
  }

  .footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: var(--space-xxl);
    margin-bottom: var(--space-xxl);
  }

  .footer-brand {
    display: flex;
    flex-direction: column;
    gap: var(--space-m);
  }

  .footer-logo img {
    width: 30px;
    height: 75px;
  }

  .footer-tagline {
    font-size: var(--type-body-small);
    font-style: italic;
    color: var(--color-text-secondary);
    max-width: 300px;
  }

  .footer-heading {
    font-size: var(--type-body-small);
    font-weight: var(--font-weight-medium);
    margin-bottom: var(--space-s);
    color: var(--color-text);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .footer-links ul,
  .footer-social ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: var(--space-s);
  }

  .footer-link {
    font-size: var(--type-body-small);
    color: var(--color-text-secondary);
    text-decoration: none;
    transition: color var(--transition-duration) var(--transition-easing);
  }

  .footer-link:hover {
    color: var(--color-accent);
  }

  .footer-copyright {
    padding-top: var(--space-l);
    border-top: var(--stroke-weight) solid var(--line-color);
    text-align: center;
  }

  .footer-copyright p {
    font-size: var(--type-micro);
    color: var(--color-text-secondary);
    margin: 0;
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .footer-grid {
      grid-template-columns: 1fr 1fr;
    }

    .footer-brand {
      grid-column: 1 / -1;
    }
  }

  @media (max-width: 768px) {
    .footer {
      padding: var(--space-l) 0;
      margin-top: var(--space-xxl);
    }

    .footer-grid {
      grid-template-columns: 1fr;
      gap: var(--space-l);
    }

    .footer-logo img {
      width: 25px;
      height: 63px;
    }
  }
</style>
