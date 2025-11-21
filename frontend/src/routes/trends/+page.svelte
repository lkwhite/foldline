<script lang="ts">
	import { apiGet } from '$lib/api';

	let metric = 'sleep_duration';
	let startDate = '2024-01-01';
	let endDate = '2025-01-01';
	let timeseriesData: any[] = [];
	let loading = false;

	const metricOptions = [
		{ value: 'sleep_duration', label: 'Sleep Duration' },
		{ value: 'resting_hr', label: 'Resting Heart Rate' },
		{ value: 'hrv', label: 'HRV' },
		{ value: 'stress', label: 'Stress' },
		{ value: 'steps', label: 'Steps' }
	];

	async function loadTrend() {
		loading = true;
		try {
			const params = new URLSearchParams({
				metric,
				start_date: startDate,
				end_date: endDate
			});
			timeseriesData = await apiGet(`/metrics/timeseries?${params}`);
		} catch (error) {
			console.error('Failed to load trend:', error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="container">
	<h1>Trends</h1>

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

		<button on:click={loadTrend} disabled={loading}>
			{loading ? 'Loading...' : 'Load Trend'}
		</button>
	</div>

	<div class="card visualization">
		{#if loading}
			<p>Loading time series data...</p>
		{:else if timeseriesData.length > 0}
			<h3>Time Series Preview (stub)</h3>
			<p class="hint">
				TODO: Add actual line chart visualization using Chart.js, Plotly, or similar library
			</p>
			<div class="data-preview">
				<p>Data points: {timeseriesData.length}</p>
				<pre>{JSON.stringify(timeseriesData.slice(0, 5), null, 2)}</pre>
			</div>
		{:else}
			<p class="hint">Click "Load Trend" to visualize your data</p>
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
