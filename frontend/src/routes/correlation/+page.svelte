<script lang="ts">
	import { apiGet } from '$lib/api';
	import FeatureGate from '$lib/components/FeatureGate.svelte';

	let xMetric = 'sleep_duration';
	let yMetric = 'resting_hr';
	let lagDays = 0;
	let correlationData: any = null;
	let loading = false;

	const metricOptions = [
		{ value: 'sleep_duration', label: 'Sleep Duration' },
		{ value: 'resting_hr', label: 'Resting Heart Rate' },
		{ value: 'hrv', label: 'HRV' },
		{ value: 'stress', label: 'Stress' },
		{ value: 'steps', label: 'Steps' }
	];

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
		<div class="card">
			<p>Analyzing correlation...</p>
		</div>
	{:else if correlationData}
		<div class="results-grid">
			<div class="card stats-card">
				<h3>Correlation Statistics</h3>
				<div class="stat-row">
					<span>Pearson r:</span>
					<span class="stat-value">{correlationData.stats.pearson_r.toFixed(3)}</span>
				</div>
				<div class="stat-row">
					<span>Pearson p:</span>
					<span class="stat-value">{correlationData.stats.pearson_p.toFixed(4)}</span>
				</div>
				<div class="stat-row">
					<span>Spearman r:</span>
					<span class="stat-value">{correlationData.stats.spearman_r.toFixed(3)}</span>
				</div>
				<div class="stat-row">
					<span>Spearman p:</span>
					<span class="stat-value">{correlationData.stats.spearman_p.toFixed(4)}</span>
				</div>
				<div class="stat-row">
					<span>Sample size:</span>
					<span class="stat-value">{correlationData.stats.n}</span>
				</div>
			</div>

			<div class="card visualization">
				<h3>Scatter Plot (stub)</h3>
				<p class="hint">
					TODO: Add actual scatter plot visualization using Chart.js or Plotly
				</p>
				<div class="data-preview">
					<p>Data points: {correlationData.x_values.length}</p>
				</div>
			</div>
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
		min-height: 400px;
	}

	.hint {
		color: var(--color-text-secondary);
		font-style: italic;
		margin-bottom: var(--spacing);
	}

	.data-preview {
		padding: var(--spacing);
		background-color: var(--color-bg);
		border-radius: var(--border-radius);
	}

	@media (max-width: 768px) {
		.results-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
