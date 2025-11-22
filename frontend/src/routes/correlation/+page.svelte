<script lang="ts">
	import { apiGet } from '$lib/api';
	import FeatureGate from '$lib/components/FeatureGate.svelte';
	import ScatterPlot from '$lib/components/ScatterPlot.svelte';

	let xMetric = 'sleep_duration';
	let yMetric = 'resting_hr';
	let lagDays = 0;
	let correlationData: any = null;
	let loading = false;
	let theme: 'light' | 'dark' = 'light';

	const metricOptions = [
		{ value: 'sleep_duration', label: 'Sleep Duration', unit: 'hours' },
		{ value: 'resting_hr', label: 'Resting Heart Rate', unit: 'bpm' },
		{ value: 'hrv', label: 'HRV', unit: 'ms' },
		{ value: 'stress', label: 'Stress', unit: 'level' },
		{ value: 'steps', label: 'Steps', unit: 'steps' }
	];

	$: selectedXMetric = metricOptions.find((m) => m.value === xMetric);
	$: selectedYMetric = metricOptions.find((m) => m.value === yMetric);
	$: chartTitle = selectedXMetric && selectedYMetric
		? `${selectedXMetric.label} vs ${selectedYMetric.label}`
		: 'Correlation';
	$: xAxisLabel = selectedXMetric
		? `${selectedXMetric.label} (${selectedXMetric.unit})`
		: 'X Metric';
	$: yAxisLabel = selectedYMetric
		? `${selectedYMetric.label} (${selectedYMetric.unit})`
		: 'Y Metric';

	// Transform API data to scatter plot format
	$: scatterData = correlationData && correlationData.x_values && correlationData.y_values
		? correlationData.x_values.map((x: number, i: number) => ({
			x,
			y: correlationData.y_values[i],
			date: correlationData.dates ? correlationData.dates[i] : undefined
		}))
		: [];

	$: correlationStats = correlationData?.stats || {};

	async function loadCorrelation() {
		loading = true;
		try {
			const params = new URLSearchParams({
				x_metric: xMetric,
				y_metric: yMetric,
				lag_days: lagDays.toString()
			});
			correlationData = await apiGet(`/metrics/correlation?${params}`);
		} catch (error) {
			console.error('Failed to load correlation:', error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="container">
	<h1>Correlation Analysis</h1>

	<FeatureGate feature="correlation_analysis" fallback="inline">
	<div class="card controls">
		<div class="control-group">
			<label for="x-metric">X-Axis Metric:</label>
			<select id="x-metric" bind:value={xMetric}>
				{#each metricOptions as option}
					<option value={option.value}>{option.label}</option>
				{/each}
			</select>
		</div>

		<div class="control-group">
			<label for="y-metric">Y-Axis Metric:</label>
			<select id="y-metric" bind:value={yMetric}>
				{#each metricOptions as option}
					<option value={option.value}>{option.label}</option>
				{/each}
			</select>
		</div>

		<div class="control-group">
			<label for="lag">Lag (days):</label>
			<input id="lag" type="number" min="0" max="30" bind:value={lagDays} />
		</div>

		<button on:click={loadCorrelation} disabled={loading}>
			{loading ? 'Analyzing...' : 'Analyze'}
		</button>
	</div>

	{#if loading}
		<div class="card loading-state">
			<p>Analyzing correlation...</p>
		</div>
	{:else if correlationData}
		<div class="results-grid">
			<div class="card stats-card">
				<h3>Correlation Statistics</h3>
				{#if correlationStats.pearson_r !== undefined}
					<div class="stat-row">
						<span>Pearson r:</span>
						<span class="stat-value">{correlationStats.pearson_r.toFixed(3)}</span>
					</div>
				{/if}
				{#if correlationStats.pearson_p !== undefined}
					<div class="stat-row">
						<span>Pearson p:</span>
						<span class="stat-value">{correlationStats.pearson_p.toFixed(4)}</span>
					</div>
				{/if}
				{#if correlationStats.spearman_r !== undefined}
					<div class="stat-row">
						<span>Spearman ρ:</span>
						<span class="stat-value">{correlationStats.spearman_r.toFixed(3)}</span>
					</div>
				{/if}
				{#if correlationStats.spearman_p !== undefined}
					<div class="stat-row">
						<span>Spearman p:</span>
						<span class="stat-value">{correlationStats.spearman_p.toFixed(4)}</span>
					</div>
				{/if}
				{#if correlationStats.n !== undefined}
					<div class="stat-row">
						<span>Sample size:</span>
						<span class="stat-value">{correlationStats.n}</span>
					</div>
				{/if}
				{#if lagDays > 0}
					<div class="stat-row">
						<span>Lag:</span>
						<span class="stat-value">{lagDays} days</span>
					</div>
				{/if}
			</div>

			<div class="card visualization">
				<ScatterPlot
					data={scatterData}
					title={chartTitle}
					{xAxisLabel}
					{yAxisLabel}
					showTrendLine={true}
					{correlationStats}
					{theme}
				/>
			</div>
		</div>
	{:else}
		<div class="card empty-state">
			<p class="hint">Select two metrics and click "Analyze" to see correlation</p>
		</div>
	{/if}
	</FeatureGate>
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

	.results-grid {
		display: grid;
		grid-template-columns: 1fr 2fr;
		gap: var(--spacing);
	}

	.stats-card {
		background-color: var(--color-bg-secondary);
	}

	.stat-row {
		display: flex;
		justify-content: space-between;
		padding: 8px 0;
		border-bottom: 1px solid var(--color-border);
	}

	.stat-row:last-child {
		border-bottom: none;
	}

	.stat-value {
		font-weight: 600;
		color: var(--color-primary);
	}

	.visualization {
		min-height: 500px;
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

	@media (max-width: 768px) {
		.results-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
