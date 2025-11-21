<script lang="ts">
	import { apiGet, apiPost } from '$lib/api';
	import { selectDataRoot } from '$lib/fileDialog';
	import { onMount } from 'svelte';

	let status: any = null;
	let dataRoot = '';
	let loading = true;
	let saving = false;
	let message = '';

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
</style>
