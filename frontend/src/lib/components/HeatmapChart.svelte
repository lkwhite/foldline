<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Plotly from 'plotly.js-dist-min';

	export let data: { date: string; value: number }[] = [];
	export let title: string = 'Heatmap';
	export let colorScale: string = 'Blues';
	export let valueLabel: string = 'Value';
	export let theme: 'light' | 'dark' = 'light';

	let chartDiv: HTMLDivElement;
	let plotlyInstance: any = null;

	$: if (plotlyInstance && data) {
		updateChart();
	}

	$: if (plotlyInstance && theme) {
		updateTheme();
	}

	interface CalendarData {
		week: number;
		day: number;
		value: number;
		date: string;
	}

	function prepareCalendarData(): CalendarData[] {
		if (!data || data.length === 0) return [];

		return data.map((d) => {
			const date = new Date(d.date);
			// Get ISO week number
			const onejan = new Date(date.getFullYear(), 0, 1);
			const week = Math.ceil(((date.getTime() - onejan.getTime()) / 86400000 + onejan.getDay() + 1) / 7);
			// Get day of week (0 = Monday, 6 = Sunday)
			const day = (date.getDay() + 6) % 7;

			return {
				week,
				day,
				value: d.value,
				date: d.date
			};
		});
	}

	function updateChart() {
		if (!chartDiv || !data || data.length === 0) return;

		const calendarData = prepareCalendarData();

		// Group by year if needed
		const years = [...new Set(calendarData.map((d) => new Date(d.date).getFullYear()))];

		if (years.length === 1) {
			// Single year - simple heatmap
			renderSingleYearHeatmap(calendarData);
		} else {
			// Multiple years - faceted heatmap
			renderMultiYearHeatmap(calendarData, years);
		}
	}

	function renderSingleYearHeatmap(calendarData: CalendarData[]) {
		// Create a matrix for the heatmap (7 days x 53 weeks)
		const matrix: (number | null)[][] = Array(7)
			.fill(null)
			.map(() => Array(53).fill(null));
		const hoverText: string[][] = Array(7)
			.fill(null)
			.map(() => Array(53).fill(''));

		calendarData.forEach((d) => {
			if (d.week >= 1 && d.week <= 53 && d.day >= 0 && d.day <= 6) {
				matrix[d.day][d.week - 1] = d.value;
				hoverText[d.day][d.week - 1] = `${d.date}<br>${valueLabel}: ${d.value.toFixed(2)}`;
			}
		});

		const trace = {
			type: 'heatmap',
			z: matrix,
			x: Array.from({ length: 53 }, (_, i) => i + 1),
			y: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
			text: hoverText,
			hovertemplate: '%{text}<extra></extra>',
			colorscale: getColorScale(),
			colorbar: {
				title: valueLabel,
				titleside: 'right',
				tickfont: {
					color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
				},
				titlefont: {
					color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
				}
			},
			showscale: true
		};

		const layout = {
			title: {
				text: title,
				font: {
					size: 18,
					color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
				}
			},
			xaxis: {
				title: 'Week of Year',
				color: theme === 'dark' ? '#9ca3af' : '#4b5563',
				showgrid: false,
				side: 'top'
			},
			yaxis: {
				title: '',
				color: theme === 'dark' ? '#9ca3af' : '#4b5563',
				showgrid: false,
				autorange: 'reversed'
			},
			plot_bgcolor: theme === 'dark' ? '#1f2937' : '#ffffff',
			paper_bgcolor: theme === 'dark' ? '#111827' : '#ffffff',
			font: {
				color: theme === 'dark' ? '#e5e7eb' : '#1f2937'
			},
			margin: {
				l: 60,
				r: 120,
				t: 80,
				b: 60
			}
		};

		const config = {
			responsive: true,
			displayModeBar: true,
			displaylogo: false,
			modeBarButtonsToRemove: ['lasso2d', 'select2d', 'zoom2d', 'pan2d'],
			toImageButtonOptions: {
				format: 'png',
				filename: title.toLowerCase().replace(/\s+/g, '_'),
				height: 400,
				width: 1200,
				scale: 2
			}
		};

		if (plotlyInstance) {
			Plotly.react(chartDiv, [trace], layout, config);
		} else {
			Plotly.newPlot(chartDiv, [trace], layout, config).then(() => {
				plotlyInstance = true;
			});
		}
	}

	function renderMultiYearHeatmap(calendarData: CalendarData[], years: number[]) {
		// For multiple years, create a simplified view showing all data points
		const sortedData = [...calendarData].sort(
			(a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
		);

		// Group by week across all years
		const weekGroups = new Map<number, { values: number[]; dates: string[] }>();

		sortedData.forEach((d) => {
			const key = d.day * 53 + d.week;
			if (!weekGroups.has(key)) {
				weekGroups.set(key, { values: [], dates: [] });
			}
			weekGroups.get(key)!.values.push(d.value);
			weekGroups.get(key)!.dates.push(d.date);
		});

		// Create matrix using average values for cells with multiple years
		const matrix: (number | null)[][] = Array(7)
			.fill(null)
			.map(() => Array(53).fill(null));
		const hoverText: string[][] = Array(7)
			.fill(null)
			.map(() => Array(53).fill(''));

		weekGroups.forEach((group, key) => {
			const day = Math.floor(key / 53);
			const week = key % 53;
			if (week >= 0 && week < 53 && day >= 0 && day < 7) {
				const avg = group.values.reduce((a, b) => a + b, 0) / group.values.length;
				matrix[day][week] = avg;
				hoverText[day][week] = `Avg ${valueLabel}: ${avg.toFixed(2)}<br>${group.dates.length} data points`;
			}
		});

		renderSingleYearHeatmap(calendarData.filter((d) => new Date(d.date).getFullYear() === years[0]));
	}

	function getColorScale(): Array<[number, string]> {
		const scales: Record<string, Array<[number, string]>> = {
			Blues: [
				[0, theme === 'dark' ? '#1e3a8a' : '#eff6ff'],
				[0.5, theme === 'dark' ? '#3b82f6' : '#60a5fa'],
				[1, theme === 'dark' ? '#60a5fa' : '#1e40af']
			],
			Greens: [
				[0, theme === 'dark' ? '#14532d' : '#f0fdf4'],
				[0.5, theme === 'dark' ? '#22c55e' : '#4ade80'],
				[1, theme === 'dark' ? '#4ade80' : '#15803d']
			],
			Reds: [
				[0, theme === 'dark' ? '#7f1d1d' : '#fef2f2'],
				[0.5, theme === 'dark' ? '#ef4444' : '#f87171'],
				[1, theme === 'dark' ? '#f87171' : '#991b1b']
			],
			Purples: [
				[0, theme === 'dark' ? '#581c87' : '#faf5ff'],
				[0.5, theme === 'dark' ? '#a855f7' : '#c084fc'],
				[1, theme === 'dark' ? '#c084fc' : '#6b21a8']
			],
			Viridis: [
				[0, '#440154'],
				[0.25, '#31688e'],
				[0.5, '#35b779'],
				[0.75, '#fde724'],
				[1, '#fde724']
			]
		};

		return scales[colorScale] || scales.Blues;
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
