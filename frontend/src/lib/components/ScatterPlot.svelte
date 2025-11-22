<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Plotly from 'plotly.js-dist-min';

	export let data: { x: number; y: number; date?: string }[] = [];
	export let title: string = 'Correlation';
	export let xAxisLabel: string = 'X Metric';
	export let yAxisLabel: string = 'Y Metric';
	export let showTrendLine: boolean = true;
	export let correlationStats: { pearson?: number; spearman?: number; pValue?: number } = {};
	export let theme: 'light' | 'dark' = 'light';

	let chartDiv: HTMLDivElement;
	let plotlyInstance: any = null;

	$: if (plotlyInstance && data) {
		updateChart();
	}

	$: if (plotlyInstance && theme) {
		updateTheme();
	}

	function calculateTrendLine(): { x: number[]; y: number[] } | null {
		if (!data || data.length < 2) return null;

		// Extract x and y values
		const xValues = data.map((d) => d.x);
		const yValues = data.map((d) => d.y);

		// Calculate linear regression
		const n = xValues.length;
		const sumX = xValues.reduce((a, b) => a + b, 0);
		const sumY = yValues.reduce((a, b) => a + b, 0);
		const sumXY = xValues.reduce((sum, x, i) => sum + x * yValues[i], 0);
		const sumX2 = xValues.reduce((sum, x) => sum + x * x, 0);

		const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
		const intercept = (sumY - slope * sumX) / n;

		// Generate trend line points
		const minX = Math.min(...xValues);
		const maxX = Math.max(...xValues);
		const trendX = [minX, maxX];
		const trendY = trendX.map((x) => slope * x + intercept);

		return { x: trendX, y: trendY };
	}

	function updateChart() {
		if (!chartDiv || !data || data.length === 0) return;

		const traces: any[] = [];

		// Scatter plot trace
		traces.push({
			type: 'scatter',
			mode: 'markers',
			x: data.map((d) => d.x),
			y: data.map((d) => d.y),
			name: 'Data points',
			marker: {
				size: 8,
				color: theme === 'dark' ? '#60a5fa' : '#3b82f6',
				opacity: 0.6,
				line: {
					color: theme === 'dark' ? '#1e40af' : '#1e3a8a',
					width: 1
				}
			},
			text: data.map((d) => (d.date ? d.date : '')),
			hovertemplate:
				'<b>%{text}</b><br>' +
				xAxisLabel +
				': %{x:.2f}<br>' +
				yAxisLabel +
				': %{y:.2f}<extra></extra>'
		});

		// Trend line trace
		if (showTrendLine) {
			const trendLine = calculateTrendLine();
			if (trendLine) {
				traces.push({
					type: 'scatter',
					mode: 'lines',
					x: trendLine.x,
					y: trendLine.y,
					name: 'Trend line',
					line: {
						color: theme === 'dark' ? '#f97316' : '#ea580c',
						width: 2,
						dash: 'dash'
					},
					hoverinfo: 'skip'
				});
			}
		}

		// Build title with correlation stats if available
		let titleText = title;
		if (correlationStats.pearson !== undefined || correlationStats.spearman !== undefined) {
			const stats: string[] = [];
			if (correlationStats.pearson !== undefined) {
				stats.push(`r=${correlationStats.pearson.toFixed(3)}`);
			}
			if (correlationStats.spearman !== undefined) {
				stats.push(`ρ=${correlationStats.spearman.toFixed(3)}`);
			}
			if (correlationStats.pValue !== undefined) {
				stats.push(`p=${correlationStats.pValue.toFixed(4)}`);
			}
			if (stats.length > 0) {
				titleText = `${title} (${stats.join(', ')})`;
			}
		}

		const layout = {
			title: {
				text: titleText,
				font: {
					size: 18,
					color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
				}
			},
			xaxis: {
				title: xAxisLabel,
				color: theme === 'dark' ? '#9ca3af' : '#4b5563',
				gridcolor: theme === 'dark' ? '#374151' : '#e5e7eb',
				showgrid: true,
				zeroline: false
			},
			yaxis: {
				title: yAxisLabel,
				color: theme === 'dark' ? '#9ca3af' : '#4b5563',
				gridcolor: theme === 'dark' ? '#374151' : '#e5e7eb',
				showgrid: true,
				zeroline: false
			},
			plot_bgcolor: theme === 'dark' ? '#1f2937' : '#ffffff',
			paper_bgcolor: theme === 'dark' ? '#111827' : '#ffffff',
			font: {
				color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
			},
			hovermode: 'closest',
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
				width: 800,
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
			<p>No data available for correlation analysis</p>
			<p class="hint">Select two metrics and load data to see correlation</p>
		</div>
	{/if}
</div>

<style>
	.chart-wrapper {
		width: 100%;
		min-height: 500px;
		position: relative;
	}

	.chart-container {
		width: 100%;
		height: 100%;
		min-height: 500px;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 500px;
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
