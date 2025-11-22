<script lang="ts">
  import { license } from '$lib/stores/license';
  import { createEventDispatcher } from 'svelte';

  export let show = true;
  export let allowSkip = true;

  const dispatch = createEventDispatcher();

  let licenseKey = '';
  let error = '';
  let isActivating = false;

  function validateLicenseKey(key: string): boolean {
    // TODO: Replace with actual Lemon Squeezy validation
    // For MVP: accept any non-empty key
    if (!key || key.trim().length === 0) {
      return false;
    }

    // Basic format validation: should look like XXXX-XXXX-XXXX-XXXX
    // But we're lenient for now
    return key.trim().length >= 4;
  }

  async function handleActivate() {
    error = '';

    if (!validateLicenseKey(licenseKey)) {
      error = 'Please enter a valid license key';
      return;
    }

    isActivating = true;

    try {
      // TODO: Optional API validation in the future
      // For now, trust-based activation
      await new Promise(resolve => setTimeout(resolve, 500)); // Simulate validation delay

      license.activate(licenseKey.trim());
      dispatch('activated');
      show = false;
    } catch (err) {
      error = 'Activation failed. Please try again or contact support.';
    } finally {
      isActivating = false;
    }
  }

  function handleSkip() {
    dispatch('skipped');
    show = false;
  }

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' && !isActivating) {
      handleActivate();
    }
  }
</script>

{#if show}
  <div class="modal-overlay" on:click|self={allowSkip ? handleSkip : null}>
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">Activate Foldline</h2>
      </div>

      <div class="modal-body">
        <p class="activation-description">
          Enter the license key from your purchase email to unlock full functionality.
        </p>

        <div class="input-container">
          <label for="license-key" class="visually-hidden">License Key</label>
          <input
            id="license-key"
            type="text"
            placeholder="XXXX-XXXX-XXXX-XXXX"
            bind:value={licenseKey}
            on:keypress={handleKeyPress}
            disabled={isActivating}
            class="license-input"
            autocomplete="off"
            spellcheck="false"
          />
        </div>

        {#if error}
          <p class="error-message">{error}</p>
        {/if}

        <div class="button-group">
          <button
            class="btn btn-cta"
            on:click={handleActivate}
            disabled={isActivating || !licenseKey.trim()}
          >
            {isActivating ? 'Activating...' : 'Activate'}
          </button>

          {#if allowSkip}
            <button class="btn btn-secondary" on:click={handleSkip} disabled={isActivating}>
              Skip for now
            </button>
          {/if}
        </div>

        <div class="privacy-note">
          <p class="privacy-text">
            <strong>Your data never leaves this device.</strong>
            This is a one-time activation only. No telemetry, no tracking, no continuous server calls.
          </p>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
  }

  .modal-content {
    background-color: var(--color-bg);
    border: var(--stroke-weight) solid var(--line-color);
    border-radius: var(--border-radius-medium);
    max-width: 500px;
    width: calc(100% - var(--space-xl) * 2);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  }

  .modal-header {
    padding: var(--space-xl);
    border-bottom: var(--stroke-weight) solid var(--line-color);
  }

  .modal-title {
    font-size: var(--type-h2);
    font-weight: var(--font-weight-medium);
    color: var(--color-text);
    margin: 0;
  }

  .modal-body {
    padding: var(--space-xl);
    display: flex;
    flex-direction: column;
    gap: var(--space-l);
  }

  .activation-description {
    font-size: var(--type-body);
    line-height: var(--line-height-normal);
    color: var(--color-text-secondary);
    margin: 0;
  }

  .input-container {
    display: flex;
    flex-direction: column;
  }

  .license-input {
    width: 100%;
    padding: 12px 16px;
    font-family: 'Inter', monospace;
    font-size: var(--type-body);
    font-variant-numeric: tabular-nums;
    letter-spacing: 0.05em;
    text-align: center;
    background-color: var(--color-bg);
    color: var(--color-text);
    border: var(--stroke-weight) solid var(--line-color);
    border-radius: var(--border-radius-medium);
    transition: border-color var(--transition-duration) var(--transition-easing);
  }

  .license-input:focus {
    outline: none;
    border-color: var(--color-accent);
  }

  .license-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .license-input::placeholder {
    color: var(--color-text-secondary);
    opacity: 0.5;
  }

  .error-message {
    padding: var(--space-s) var(--space-m);
    background-color: rgba(255, 59, 48, 0.1);
    border: var(--stroke-weight) solid rgba(255, 59, 48, 0.3);
    border-radius: var(--border-radius-small);
    color: #ff3b30;
    font-size: var(--type-body-small);
    margin: 0;
  }

  .button-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-m);
  }

  .button-group .btn {
    width: 100%;
    padding: 12px 24px;
    justify-content: center;
  }

  .privacy-note {
    padding-top: var(--space-l);
    border-top: var(--stroke-weight) solid var(--line-color);
  }

  .privacy-text {
    font-size: var(--type-body-small);
    line-height: var(--line-height-relaxed);
    color: var(--color-text-secondary);
    text-align: center;
    margin: 0;
  }

  .privacy-text strong {
    color: var(--color-text);
  }

  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  @media (max-width: 768px) {
    .modal-content {
      max-width: none;
      width: calc(100% - var(--space-m) * 2);
    }

    .modal-header,
    .modal-body {
      padding: var(--space-l);
    }

    .modal-title {
      font-size: var(--type-h3);
    }

    .license-input {
      font-size: var(--type-body-small);
    }
  }
</style>
