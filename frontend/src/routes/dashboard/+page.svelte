<script lang="ts">
	import { onMount } from 'svelte';
	import { apiGet } from '$lib/api';

	let status: any = null;
	let loading = true;
	let error = '';

	onMount(async () => {
		try {
			status = await apiGet('/status');
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	});
</script>

<div class="container">
	<h1>Dashboard</h1>

	{#if loading}
		<div class="card">
			<p>Loading status...</p>
		</div>
	{:else if error}
		<div class="card error-card">
			<p>Error: {error}</p>
		</div>
	{:else if status}
		<div class="dashboard-grid">
			<div class="card stat-card">
				<h3>Database</h3>
				<p class="stat-value">{status.db_initialized ? '✓ Initialized' : '✗ Not initialized'}</p>
			</div>

			<div class="card stat-card">
				<h3>Date Range</h3>
				<p class="stat-value">{status.min_date} to {status.max_date}</p>
			</div>

			<div class="card stat-card">
				<h3>Sleep Records</h3>
				<p class="stat-value">{status.counts.nights.toLocaleString()} nights</p>
			</div>

			<div class="card stat-card">
				<h3>Activities</h3>
				<p class="stat-value">{status.counts.activities.toLocaleString()} activities</p>
			</div>

			<div class="card stat-card">
				<h3>Days with Data</h3>
				<p class="stat-value">{status.counts.days_with_data.toLocaleString()} days</p>
			</div>

			<div class="card metrics-card">
				<h3>Available Metrics</h3>
				<ul>
					{#each status.available_metrics as metric}
						<li>{metric}</li>
					{/each}
				</ul>
			</div>
		</div>
	{/if}
</div>

<style>
	.dashboard-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: var(--spacing);
		margin-top: calc(var(--spacing) * 2);
	}

	.stat-card {
		text-align: center;
	}

	.stat-card h3 {
		color: var(--color-text-secondary);
		font-size: 0.9rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.stat-value {
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--color-primary);
		margin-top: calc(var(--spacing) * 0.5);
	}

	.metrics-card {
		grid-column: span 2;
	}

	.metrics-card ul {
		list-style: none;
		display: flex;
		flex-wrap: wrap;
		gap: calc(var(--spacing) * 0.5);
	}

	.metrics-card li {
		background-color: var(--color-bg);
		padding: 8px 16px;
		border-radius: var(--border-radius);
		border: 1px solid var(--color-border);
	}

	.error-card {
		background-color: rgba(244, 67, 54, 0.1);
		border-color: var(--color-error);
	}
</style>
