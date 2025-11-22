<script lang="ts">
  import { license, type PremiumFeature } from '$lib/stores/license';
  import UpgradePrompt from './UpgradePrompt.svelte';
  import LicenseActivationModal from './LicenseActivationModal.svelte';

  export let feature: PremiumFeature;
  export let fallback: 'inline' | 'banner' | 'hide' = 'inline';

  let showLicenseModal = false;

  $: hasAccess = $license.isActivated;

  function handleUpgrade() {
    showLicenseModal = true;
  }

  function handleActivated() {
    showLicenseModal = false;
  }
</script>

{#if hasAccess}
  <!-- User has premium, show the gated content -->
  <slot />
{:else if fallback === 'inline'}
  <!-- Show inline upgrade prompt instead of content -->
  <UpgradePrompt {feature} inline={true} on:upgrade={handleUpgrade} />
{:else if fallback === 'banner'}
  <!-- Show banner above content (content is still visible but limited) -->
  <UpgradePrompt {feature} inline={false} on:upgrade={handleUpgrade} />
  <slot name="limited" />
{:else}
  <!-- Hide content completely, show nothing -->
{/if}

<LicenseActivationModal
  bind:show={showLicenseModal}
  allowSkip={true}
  on:activated={handleActivated}
/>
