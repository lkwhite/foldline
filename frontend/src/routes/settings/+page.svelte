<script lang="ts">
	import { apiGet, apiPost } from '$lib/api';
	import { selectDataRoot } from '$lib/fileDialog';
	import { onMount } from 'svelte';
	import { license } from '$lib/stores/license';
	import LicenseActivationModal from '$lib/components/LicenseActivationModal.svelte';

	let status: any = null;
	let dataRoot = '';
	let loading = true;
	let saving = false;
	let message = '';
	let showLicenseModal = false;

	function handleChangeLicense() {
		showLicenseModal = true;
	}

	function handleDeactivate() {
		if (confirm('Are you sure you want to deactivate your license? You can reactivate it later.')) {
			license.deactivate();
		}
	}

	function handleLicenseActivated() {
		showLicenseModal = false;
	}

	onMount(async () => {
		try {
			status = await apiGet('/status');
		} catch (error) {
			console.error('Failed to load status:', error);
		} finally {
			loading = false;
		}
	});

	async function handleSelectDataRoot() {
		const selected = await selectDataRoot();
		if (selected) {
			dataRoot = selected;
		}
	}

	async function handleSaveDataRoot() {
		if (!dataRoot) {
			message = 'Please select a data root directory';
			return;
		}

		saving = true;
		message = '';

		try {
			const result = await apiPost('/settings/data-root', { data_root: dataRoot });
			message = 'Data root updated successfully';
		} catch (error: any) {
			message = `Error: ${error.message}`;
		} finally {
			saving = false;
		}
	}
</script>

<div class="container">
	<h1>Settings</h1>

	{#if loading}
		<div class="card">
			<p>Loading settings...</p>
		</div>
	{:else}
		<div class="settings-section">
			<div class="card">
				<h2>Data Storage</h2>
				<p class="description">
					Choose where Foldline stores its database and imported data files.
				</p>

				<div class="setting-control">
					<label for="data-root">Data Root Directory:</label>
					<div class="input-group">
						<input id="data-root" type="text" bind:value={dataRoot} readonly />
						<button on:click={handleSelectDataRoot}>Browse</button>
					</div>
				</div>

				<button on:click={handleSaveDataRoot} disabled={saving || !dataRoot}>
					{saving ? 'Saving...' : 'Save Changes'}
				</button>

				{#if message}
					<p class="message">{message}</p>
				{/if}
			</div>

			<div class="card">
				<h2>Current Status</h2>
				<div class="status-grid">
					<div class="status-item">
						<span class="label">Database:</span>
						<span>{status?.db_initialized ? 'Initialized' : 'Not initialized'}</span>
					</div>
					<div class="status-item">
						<span class="label">Available Metrics:</span>
						<span>{status?.available_metrics.length || 0}</span>
					</div>
					<div class="status-item">
						<span class="label">Data Range:</span>
						<span>{status?.min_date} to {status?.max_date}</span>
					</div>
				</div>
			</div>

			<div class="card">
				<h2>License</h2>
				<p class="description">
					Manage your Foldline license activation.
				</p>

				<div class="status-grid">
					<div class="status-item">
						<span class="label">Status:</span>
						<span class:activated={$license.isActivated}>
							{$license.isActivated ? '✓ Activated' : 'Not activated'}
						</span>
					</div>
					{#if $license.isActivated}
						<div class="status-item">
							<span class="label">License Key:</span>
							<span class="license-key">{license.getMaskedKey($license.licenseKey || '')}</span>
						</div>
						<div class="status-item">
							<span class="label">Activated:</span>
							<span>{new Date($license.activatedAt || '').toLocaleDateString()}</span>
						</div>
					{/if}
				</div>

				<div class="button-group">
					{#if $license.isActivated}
						<button on:click={handleChangeLicense} class="btn-secondary">
							Change License
						</button>
						<button on:click={handleDeactivate} class="btn-danger">
							Deactivate
						</button>
					{:else}
						<button on:click={handleChangeLicense} class="btn-primary">
							Activate License
						</button>
					{/if}
				</div>
			</div>

			<div class="card info-card">
				<h2>About Data Storage</h2>
				<p>
					All your data is stored locally in the data root directory. You can change this
					location at any time, but you'll need to re-import your data if you move it.
				</p>
				<p>
					Foldline never uploads your data to any external servers. Everything stays on your
					machine.
				</p>
			</div>
		</div>
	{/if}
</div>

<LicenseActivationModal
	bind:show={showLicenseModal}
	allowSkip={$license.isActivated}
	on:activated={handleLicenseActivated}
/>

<style>
	.settings-section {
		max-width: 800px;
		display: flex;
		flex-direction: column;
		gap: var(--spacing);
	}

	.description {
		color: var(--color-text-secondary);
		margin-bottom: var(--spacing);
	}

	.setting-control {
		margin-bottom: var(--spacing);
	}

	.setting-control label {
		display: block;
		margin-bottom: 8px;
		color: var(--color-text-secondary);
	}

	.input-group {
		display: flex;
		gap: 8px;
	}

	.input-group input {
		flex: 1;
	}

	.message {
		margin-top: var(--spacing);
		padding: 8px 12px;
		background-color: var(--color-bg);
		border-radius: var(--border-radius);
		border: 1px solid var(--color-border);
	}

	.status-grid {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.status-item {
		display: flex;
		justify-content: space-between;
		padding: 8px 0;
		border-bottom: 1px solid var(--color-border);
	}

	.status-item:last-child {
		border-bottom: none;
	}

	.label {
		color: var(--color-text-secondary);
	}

	.info-card {
		background-color: rgba(74, 144, 226, 0.1);
		border-color: var(--color-primary);
	}

	.info-card p {
		margin-bottom: 8px;
	}

	.info-card p:last-child {
		margin-bottom: 0;
	}

	/* License section styles */
	.button-group {
		display: flex;
		gap: 8px;
		margin-top: var(--spacing);
	}

	.button-group button {
		flex: 1;
	}

	.btn-primary {
		background-color: var(--color-accent, #E69F00);
		color: #ffffff;
		padding: 10px 20px;
		border: none;
		border-radius: var(--border-radius-medium, 4px);
		cursor: pointer;
		font-weight: var(--font-weight-medium, 500);
		transition: background-color var(--transition-duration, 200ms) var(--transition-easing, ease);
	}

	.btn-primary:hover {
		background-color: var(--color-accent-hover, #d18e00);
	}

	.btn-secondary {
		background-color: transparent;
		color: var(--color-text);
		padding: 10px 20px;
		border: var(--stroke-weight, 1px) solid var(--line-color);
		border-radius: var(--border-radius-medium, 4px);
		cursor: pointer;
		font-weight: var(--font-weight-medium, 500);
		transition: border-color var(--transition-duration, 200ms) var(--transition-easing, ease);
	}

	.btn-secondary:hover {
		border-color: var(--color-accent, #E69F00);
		color: var(--color-accent, #E69F00);
	}

	.btn-danger {
		background-color: transparent;
		color: #ff3b30;
		padding: 10px 20px;
		border: var(--stroke-weight, 1px) solid rgba(255, 59, 48, 0.3);
		border-radius: var(--border-radius-medium, 4px);
		cursor: pointer;
		font-weight: var(--font-weight-medium, 500);
		transition: all var(--transition-duration, 200ms) var(--transition-easing, ease);
	}

	.btn-danger:hover {
		border-color: #ff3b30;
		background-color: rgba(255, 59, 48, 0.1);
	}

	.license-key {
		font-family: 'Inter', monospace;
		font-variant-numeric: tabular-nums;
		letter-spacing: 0.05em;
		color: var(--color-text);
	}

	.activated {
		color: var(--color-accent, #E69F00);
		font-weight: var(--font-weight-medium, 500);
	}
</style>
