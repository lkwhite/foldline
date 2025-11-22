<script lang="ts">
  import { onMount } from 'svelte';

  // TODO: Replace with actual Lemon Squeezy checkout URL from environment variable
  // In production, this should come from: import.meta.env.LEMONSQUEEZY_CHECKOUT_URL
  const CHECKOUT_URL = 'https://foldline.lemonsqueezy.com/checkout/buy/PLACEHOLDER';

  let minAmount = 15; // Configurable minimum PWYW amount

  function handleCheckout() {
    // TODO: Implement dynamic checkout with user-selected amount (optional enhancement)
    // For now, just open the static checkout URL
    window.open(CHECKOUT_URL, '_blank');
  }
</script>

<svelte:head>
  <title>Buy Foldline - Privacy-First Wearable Data Analyzer</title>
  <meta name="description" content="Get Foldline with a one-time payment. No subscriptions, no tracking, no cloud uploads. 10% of revenue supports the EFF." />
</svelte:head>

<section class="buy-section">
  <div class="container">
    <!-- Header -->
    <div class="buy-header">
      <h1 class="buy-title">Get Foldline</h1>
      <p class="buy-subtitle">
        One-time purchase. Lifetime access. Your data stays local.
      </p>
    </div>

    <!-- Pricing Card -->
    <div class="pricing-card">
      <div class="pricing-content">
        <div class="pricing-header">
          <h2 class="pricing-title">Pay What You Want</h2>
          <p class="pricing-amount">Suggested: ${minAmount}+ USD</p>
        </div>

        <div class="pricing-features">
          <h3 class="features-title">What you get:</h3>
          <ul class="features-list">
            <li>
              <span class="feature-icon">✓</span>
              <span>Complete desktop app for macOS, Windows, and Linux</span>
            </li>
            <li>
              <span class="feature-icon">✓</span>
              <span>All features unlocked, forever</span>
            </li>
            <li>
              <span class="feature-icon">✓</span>
              <span>Future updates included</span>
            </li>
            <li>
              <span class="feature-icon">✓</span>
              <span>No subscriptions or recurring fees</span>
            </li>
            <li>
              <span class="feature-icon">✓</span>
              <span>Privacy-first: 100% local data processing</span>
            </li>
          </ul>
        </div>

        <button class="btn btn-cta btn-large" on:click={handleCheckout}>
          Continue to Secure Checkout
        </button>

        <p class="checkout-note">
          You'll be redirected to Lemon Squeezy for secure payment processing.
          After purchase, you'll receive a download link and license key via email.
        </p>
      </div>
    </div>

    <!-- Privacy & EFF Section -->
    <div class="info-grid">
      <div class="info-card">
        <h3 class="info-title">Your Privacy Matters</h3>
        <p class="info-text">
          Foldline processes all your wearable data <strong>locally on your device</strong>.
          No cloud uploads, no external API calls, no telemetry. Once you activate your
          license, the app works <strong>100% offline</strong>.
        </p>
        <p class="info-text">
          License activation is a one-time process. After that, your data never leaves your machine.
        </p>
      </div>

      <div class="info-card">
        <h3 class="info-title">Supporting Privacy Rights</h3>
        <p class="info-text">
          <strong>10% of net revenue goes to the Electronic Frontier Foundation</strong> (EFF),
          a nonprofit defending digital privacy, free expression, and innovation.
        </p>
        <p class="info-text">
          By purchasing Foldline, you're supporting the broader movement for privacy-respecting software.
        </p>
        <a
          href="https://www.eff.org"
          target="_blank"
          rel="noopener noreferrer"
          class="info-link"
        >
          Learn more about the EFF →
        </a>
      </div>
    </div>

    <!-- How It Works -->
    <div class="how-it-works">
      <h2 class="section-title">How it works</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3 class="step-title">Purchase</h3>
          <p class="step-text">
            Complete checkout with your chosen amount (minimum ${minAmount} USD).
            Payment handled securely by Lemon Squeezy.
          </p>
        </div>

        <div class="step">
          <div class="step-number">2</div>
          <h3 class="step-title">Download</h3>
          <p class="step-text">
            Receive an email with your license key and download links for
            macOS, Windows, or Linux.
          </p>
        </div>

        <div class="step">
          <div class="step-number">3</div>
          <h3 class="step-title">Activate</h3>
          <p class="step-text">
            Install the app, enter your license key once, and you're done.
            Full offline access, forever.
          </p>
        </div>
      </div>
    </div>

    <!-- FAQ -->
    <div class="faq">
      <h2 class="section-title">Common questions</h2>
      <div class="faq-list">
        <div class="faq-item">
          <h3 class="faq-question">Do I need an account?</h3>
          <p class="faq-answer">
            No. You only need your license key to activate the app. No login,
            no account, no ongoing relationship with any server.
          </p>
        </div>

        <div class="faq-item">
          <h3 class="faq-question">What if I want a refund?</h3>
          <p class="faq-answer">
            Contact support within 30 days for a full refund, no questions asked.
          </p>
        </div>

        <div class="faq-item">
          <h3 class="faq-question">Can I use Foldline on multiple devices?</h3>
          <p class="faq-answer">
            Yes. One license works on all your personal devices (macOS, Windows, Linux).
          </p>
        </div>

        <div class="faq-item">
          <h3 class="faq-question">Will my data sync between devices?</h3>
          <p class="faq-answer">
            No. Foldline is local-only by design. Your data stays on each device where you import it.
            This is a privacy feature, not a limitation.
          </p>
        </div>

        <div class="faq-item">
          <h3 class="faq-question">What wearables are supported?</h3>
          <p class="faq-answer">
            Any device that exports FIT files (Garmin, Wahoo, etc.) or connects via
            Garmin Express. More integrations coming soon.
          </p>
        </div>
      </div>
    </div>

    <!-- Back to Home -->
    <div class="back-link">
      <a href="/" class="btn btn-secondary">← Back to Home</a>
    </div>
  </div>
</section>

<style>
  .buy-section {
    padding: calc(var(--space-xxl) * 2) 0;
    min-height: 100vh;
  }

  .buy-header {
    text-align: center;
    margin-bottom: calc(var(--space-xxl) * 1.5);
  }

  .buy-title {
    font-size: var(--type-h1);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin-bottom: var(--space-m);
  }

  .buy-subtitle {
    font-size: var(--type-h3);
    color: var(--color-text-secondary);
    max-width: 600px;
    margin: 0 auto;
  }

  /* Pricing Card */
  .pricing-card {
    max-width: 640px;
    margin: 0 auto var(--space-xxl);
    background-color: var(--color-bg);
    border: var(--stroke-weight) solid var(--line-color);
    border-radius: var(--border-radius-medium);
    padding: var(--space-xxl);
  }

  .pricing-header {
    text-align: center;
    margin-bottom: var(--space-xl);
  }

  .pricing-title {
    font-size: var(--type-h2);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin-bottom: var(--space-s);
  }

  .pricing-amount {
    font-size: var(--type-h3);
    color: var(--color-accent);
    font-weight: var(--font-weight-medium);
  }

  .pricing-features {
    margin-bottom: var(--space-xl);
  }

  .features-title {
    font-size: var(--type-body);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin-bottom: var(--space-m);
  }

  .features-list {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: var(--space-m);
  }

  .features-list li {
    display: flex;
    align-items: flex-start;
    gap: var(--space-m);
    font-size: var(--type-body);
    line-height: var(--line-height-normal);
    color: var(--color-text);
  }

  .feature-icon {
    color: var(--color-accent);
    font-weight: var(--font-weight-medium);
    flex-shrink: 0;
  }

  .btn-large {
    width: 100%;
    padding: 16px 32px;
    font-size: var(--type-body);
    margin-bottom: var(--space-m);
  }

  .checkout-note {
    font-size: var(--type-body-small);
    color: var(--color-text-secondary);
    text-align: center;
    line-height: var(--line-height-normal);
  }

  /* Info Grid */
  .info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-xl);
    max-width: 1000px;
    margin: 0 auto var(--space-xxl);
  }

  .info-card {
    background-color: var(--color-bg);
    border: var(--stroke-weight) solid var(--line-color);
    border-radius: var(--border-radius-medium);
    padding: var(--space-xl);
  }

  .info-title {
    font-size: var(--type-h3);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin-bottom: var(--space-m);
  }

  .info-text {
    font-size: var(--type-body);
    line-height: var(--line-height-relaxed);
    color: var(--color-text);
    margin-bottom: var(--space-m);
  }

  .info-text:last-of-type {
    margin-bottom: 0;
  }

  .info-link {
    display: inline-flex;
    align-items: center;
    font-size: var(--type-body);
    color: var(--color-accent);
    text-decoration: none;
    margin-top: var(--space-m);
    transition: color var(--transition-duration) var(--transition-easing);
  }

  .info-link:hover {
    color: var(--color-accent-hover);
  }

  /* How It Works */
  .how-it-works {
    max-width: 900px;
    margin: 0 auto calc(var(--space-xxl) * 2);
  }

  .section-title {
    font-size: var(--type-h2);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    text-align: center;
    margin-bottom: var(--space-xxl);
  }

  .steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-xl);
  }

  .step {
    text-align: center;
  }

  .step-number {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: var(--color-accent);
    color: #ffffff;
    font-size: var(--type-h3);
    font-weight: var(--font-weight-medium);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto var(--space-m);
  }

  .step-title {
    font-size: var(--type-h3);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin-bottom: var(--space-s);
  }

  .step-text {
    font-size: var(--type-body-small);
    line-height: var(--line-height-normal);
    color: var(--color-text-secondary);
  }

  /* FAQ */
  .faq {
    max-width: 800px;
    margin: 0 auto calc(var(--space-xxl) * 2);
  }

  .faq-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-xl);
  }

  .faq-item {
    border-top: var(--stroke-weight) solid var(--line-color);
    padding-top: var(--space-l);
  }

  .faq-item:first-child {
    border-top: none;
    padding-top: 0;
  }

  .faq-question {
    font-size: var(--type-body);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin-bottom: var(--space-s);
  }

  .faq-answer {
    font-size: var(--type-body-small);
    line-height: var(--line-height-relaxed);
    color: var(--color-text-secondary);
  }

  /* Back Link */
  .back-link {
    text-align: center;
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .info-grid {
      grid-template-columns: 1fr;
    }

    .steps {
      grid-template-columns: 1fr;
      gap: var(--space-xxl);
    }
  }

  @media (max-width: 768px) {
    .buy-section {
      padding: var(--space-xxl) 0;
    }

    .buy-title {
      font-size: var(--type-h2);
    }

    .buy-subtitle {
      font-size: var(--type-body);
    }

    .pricing-card {
      padding: var(--space-xl);
    }

    .pricing-title {
      font-size: var(--type-h3);
    }

    .info-card {
      padding: var(--space-l);
    }
  }
</style>
