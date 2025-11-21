<script lang="ts">
	import { apiGet } from '$lib/api';

	let metric = 'sleep_duration';
	let startDate = '2024-01-01';
	let endDate = '2025-01-01';
	let heatmapData: any[] = [];
	let loading = false;

	const metricOptions = [
		{ value: 'sleep_duration', label: 'Sleep Duration' },
		{ value: 'resting_hr', label: 'Resting Heart Rate' },
		{ value: 'hrv', label: 'HRV' },
		{ value: 'stress', label: 'Stress' },
		{ value: 'steps', label: 'Steps' }
	];

	async function loadHeatmap() {
		loading = true;
		try {
			const params = new URLSearchParams({
				metric,
				start_date: startDate,
				end_date: endDate
			});
			heatmapData = await apiGet(`/metrics/heatmap?${params}`);
		} catch (error) {
			console.error('Failed to load heatmap:', error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="container">
	<h1>Heatmaps</h1>

	<div class="card controls">
		<div class="control-group">
			<label for="metric">Metric:</label>
			<select id="metric" bind:value={metric}>
				{#each metricOptions as option}
					<option value={option.value}>{option.label}</option>
				{/each}
			</select>
		</div>

		<div class="control-group">
			<label for="start-date">Start Date:</label>
			<input id="start-date" type="date" bind:value={startDate} />
		</div>

		<div class="control-group">
			<label for="end-date">End Date:</label>
			<input id="end-date" type="date" bind:value={endDate} />
		</div>

		<button on:click={loadHeatmap} disabled={loading}>
			{loading ? 'Loading...' : 'Load Heatmap'}
		</button>
	</div>

	<div class="card visualization">
		{#if loading}
			<p>Loading heatmap data...</p>
		{:else if heatmapData.length > 0}
			<h3>Heatmap Preview (stub)</h3>
			<p class="hint">
				TODO: Add actual heatmap visualization using D3.js, Chart.js, or similar library
			</p>
			<div class="data-preview">
				<p>Data points: {heatmapData.length}</p>
				<pre>{JSON.stringify(heatmapData.slice(0, 5), null, 2)}</pre>
			</div>
		{:else}
			<p class="hint">Click "Load Heatmap" to visualize your data</p>
		{/if}
	</div>
</div>

<style>
	.controls {
		display: flex;
		flex-wrap: wrap;
		gap: var(--spacing);
		align-items: flex-end;
		margin-bottom: var(--spacing);
	}

	.control-group {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.control-group label {
		font-size: 0.9rem;
		color: var(--color-text-secondary);
	}

	.visualization {
		min-height: 400px;
	}

	.hint {
		color: var(--color-text-secondary);
		font-style: italic;
	}

	.data-preview {
		margin-top: var(--spacing);
		padding: var(--spacing);
		background-color: var(--color-bg);
		border-radius: var(--border-radius);
	}

	.data-preview pre {
		color: var(--color-text-secondary);
		font-size: 0.85rem;
		overflow-x: auto;
	}
</style>
