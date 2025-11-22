<script lang="ts">
	import { apiGet } from '$lib/api';
	import TimeSeriesChart from '$lib/components/TimeSeriesChart.svelte';

	let metric = 'sleep_duration';
	let startDate = '2024-01-01';
	let endDate = '2025-01-01';
	let timeseriesData: any[] = [];
	let loading = false;
	let theme: 'light' | 'dark' = 'light';

	const metricOptions = [
		{ value: 'sleep_duration', label: 'Sleep Duration', unit: 'hours' },
		{ value: 'resting_hr', label: 'Resting Heart Rate', unit: 'bpm' },
		{ value: 'hrv', label: 'HRV', unit: 'ms' },
		{ value: 'stress', label: 'Stress', unit: 'level' },
		{ value: 'steps', label: 'Steps', unit: 'steps' }
	];

	$: selectedMetric = metricOptions.find((m) => m.value === metric);
	$: chartTitle = selectedMetric ? `${selectedMetric.label} Over Time` : 'Trends';
	$: yAxisLabel = selectedMetric
		? `${selectedMetric.label} (${selectedMetric.unit})`
		: 'Value';

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
			<div class="loading-state">
				<p>Loading time series data...</p>
			</div>
		{:else if timeseriesData.length > 0}
			<TimeSeriesChart
				data={timeseriesData}
				title={chartTitle}
				yAxisLabel={yAxisLabel}
				showRollingAverage={true}
				{theme}
			/>
		{:else}
			<div class="empty-state">
				<p class="hint">Click "Load Trend" to visualize your data</p>
			</div>
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

	.loading-state,
	.empty-state {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 400px;
		text-align: center;
	}

	.hint {
		color: var(--color-text-secondary);
		font-style: italic;
	}
</style>
