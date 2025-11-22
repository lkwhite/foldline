<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Plotly from 'plotly.js-dist-min';

	export let data: { date: string; value: number; avg?: number }[] = [];
	export let title: string = 'Time Series';
	export let yAxisLabel: string = 'Value';
	export let showRollingAverage: boolean = true;
	export let theme: 'light' | 'dark' = 'light';

	let chartDiv: HTMLDivElement;
	let plotlyInstance: any = null;

	$: if (plotlyInstance && data) {
		updateChart();
	}

	$: if (plotlyInstance && theme) {
		updateTheme();
	}

	function updateChart() {
		if (!chartDiv || !data || data.length === 0) return;

		const traces: any[] = [];

		// Main data trace
		traces.push({
			type: 'scatter',
			mode: 'lines+markers',
			x: data.map((d) => d.date),
			y: data.map((d) => d.value),
			name: yAxisLabel,
			line: {
				color: theme === 'dark' ? '#60a5fa' : '#3b82f6',
				width: 2
			},
			marker: {
				size: 4,
				color: theme === 'dark' ? '#60a5fa' : '#3b82f6'
			},
			hovertemplate: '<b>%{x}</b><br>' + yAxisLabel + ': %{y:.2f}<extra></extra>'
		});

		// Rolling average trace (if available)
		if (showRollingAverage && data.some((d) => d.avg !== undefined)) {
			traces.push({
				type: 'scatter',
				mode: 'lines',
				x: data.map((d) => d.date),
				y: data.map((d) => d.avg),
				name: '7-day average',
				line: {
					color: theme === 'dark' ? '#f97316' : '#ea580c',
					width: 2,
					dash: 'dash'
				},
				hovertemplate: '<b>%{x}</b><br>7-day avg: %{y:.2f}<extra></extra>'
			});
		}

		const layout = {
			title: {
				text: title,
				font: {
					size: 18,
					color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
				}
			},
			xaxis: {
				title: 'Date',
				color: theme === 'dark' ? '#9ca3af' : '#4b5563',
				gridcolor: theme === 'dark' ? '#374151' : '#e5e7eb',
				showgrid: true
			},
			yaxis: {
				title: yAxisLabel,
				color: theme === 'dark' ? '#9ca3af' : '#4b5563',
				gridcolor: theme === 'dark' ? '#374151' : '#e5e7eb',
				showgrid: true
			},
			plot_bgcolor: theme === 'dark' ? '#1f2937' : '#ffffff',
			paper_bgcolor: theme === 'dark' ? '#111827' : '#ffffff',
			font: {
				color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
			},
			hovermode: 'x unified',
			showlegend: true,
			legend: {
				orientation: 'h',
				yanchor: 'bottom',
				y: 1.02,
				xanchor: 'right',
				x: 1,
				font: {
					color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
				}
			},
			margin: {
				l: 60,
				r: 30,
				t: 80,
				b: 60
			}
		};

		const config = {
			responsive: true,
			displayModeBar: true,
			displaylogo: false,
			modeBarButtonsToRemove: ['lasso2d', 'select2d'],
			toImageButtonOptions: {
				format: 'png',
				filename: title.toLowerCase().replace(/\s+/g, '_'),
				height: 600,
				width: 1200,
				scale: 2
			}
		};

		if (plotlyInstance) {
			Plotly.react(chartDiv, traces, layout, config);
		} else {
			Plotly.newPlot(chartDiv, traces, layout, config).then(() => {
				plotlyInstance = true;
			});
		}
	}

	function updateTheme() {
		if (plotlyInstance && data && data.length > 0) {
			updateChart();
		}
	}

	onMount(() => {
		if (data && data.length > 0) {
			updateChart();
		}
	});

	onDestroy(() => {
		if (chartDiv && plotlyInstance) {
			Plotly.purge(chartDiv);
			plotlyInstance = null;
		}
	});
</script>

<div class="chart-wrapper">
	{#if data && data.length > 0}
		<div bind:this={chartDiv} class="chart-container" />
	{:else}
		<div class="empty-state">
			<p>No data available for the selected date range</p>
			<p class="hint">Try selecting a different date range or loading data first</p>
		</div>
	{/if}
</div>

<style>
	.chart-wrapper {
		width: 100%;
		min-height: 400px;
		position: relative;
	}

	.chart-container {
		width: 100%;
		height: 100%;
		min-height: 400px;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 400px;
		color: var(--color-text-secondary);
		text-align: center;
		padding: var(--spacing);
	}

	.empty-state p {
		margin: 8px 0;
	}

	.hint {
		font-size: 0.9rem;
		font-style: italic;
		opacity: 0.7;
	}
</style>
