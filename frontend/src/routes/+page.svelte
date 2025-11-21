<script lang="ts">
	import { onMount } from 'svelte';
	import { initBackend, apiPost } from '$lib/api';
	import { selectGarminExport, selectFitFolder } from '$lib/fileDialog';

	let backendReady = false;
	let importing = false;
	let importMessage = '';
	let importSummary: any = null;

	onMount(async () => {
		try {
			await initBackend();
			backendReady = true;
		} catch (error) {
			console.error('Failed to initialize backend:', error);
			importMessage = 'Error: Failed to start backend';
		}
	});

	async function handleGarminExport() {
		const zipPath = await selectGarminExport();
		if (!zipPath) return;

		importing = true;
		importMessage = `Importing from: ${zipPath}`;
		importSummary = null;

		try {
			const result = await apiPost<any>('/import/garmin-export', { zip_path: zipPath });
			importMessage = result.message;
			importSummary = result.summary;
		} catch (error: any) {
			importMessage = `Error: ${error.message}`;
		} finally {
			importing = false;
		}
	}

	async function handleFitFolder() {
		const folderPath = await selectFitFolder();
		if (!folderPath) return;

		importing = true;
		importMessage = `Importing from: ${folderPath}`;
		importSummary = null;

		try {
			const result = await apiPost<any>('/import/fit-folder', { folder_path: folderPath });
			importMessage = result.message;
			importSummary = result.summary;
		} catch (error: any) {
			importMessage = `Error: ${error.message}`;
		} finally {
			importing = false;
		}
	}
</script>

<div class="container">
	<div class="setup-page">
		<h1>Welcome to Foldline</h1>
		<p class="subtitle">Import your wearable data to get started</p>

		{#if !backendReady}
			<div class="card status-card">
				<p>⏳ Starting backend...</p>
			</div>
		{:else}
			<div class="import-section">
				<div class="card import-card">
					<h2>Garmin GDPR Export</h2>
					<p>
						Import data from your Garmin "Export My Data" archive. This includes all your
						historical data.
					</p>
					<button on:click={handleGarminExport} disabled={importing}>
						{importing ? 'Importing...' : 'Select ZIP File'}
					</button>
				</div>

				<div class="card import-card">
					<h2>FIT Files Folder</h2>
					<p>
						Import FIT files from a local directory (e.g., Garmin Express data folder). This is
						useful for ongoing syncs.
					</p>
					<button on:click={handleFitFolder} disabled={importing}>
						{importing ? 'Importing...' : 'Select Folder'}
					</button>
				</div>
			</div>

			{#if importMessage}
				<div class="card message-card">
					<h3>Import Status</h3>
					<p>{importMessage}</p>

					{#if importSummary}
						<div class="summary">
							<h4>Summary:</h4>
							<pre>{JSON.stringify(importSummary, null, 2)}</pre>
						</div>
					{/if}
				</div>
			{/if}

			<div class="card info-card">
				<h3>Privacy Note</h3>
				<p>
					All data is processed locally on your machine. Foldline never sends your data to any
					external servers or APIs.
				</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.setup-page {
		max-width: 800px;
		margin: 0 auto;
		padding: calc(var(--spacing) * 2) 0;
	}

	.subtitle {
		color: var(--color-text-secondary);
		margin-bottom: calc(var(--spacing) * 2);
		font-size: 1.1rem;
	}

	.import-section {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--spacing);
		margin-bottom: calc(var(--spacing) * 2);
	}

	.import-card h2 {
		color: var(--color-primary);
	}

	.import-card p {
		color: var(--color-text-secondary);
		margin-bottom: var(--spacing);
	}

	.status-card,
	.message-card,
	.info-card {
		margin-bottom: var(--spacing);
	}

	.info-card {
		background-color: rgba(74, 144, 226, 0.1);
		border-color: var(--color-primary);
	}

	.summary {
		margin-top: var(--spacing);
		padding: var(--spacing);
		background-color: var(--color-bg);
		border-radius: var(--border-radius);
	}

	.summary pre {
		color: var(--color-text-secondary);
		font-size: 0.9rem;
		overflow-x: auto;
	}

	@media (max-width: 768px) {
		.import-section {
			grid-template-columns: 1fr;
		}
	}
</style>
