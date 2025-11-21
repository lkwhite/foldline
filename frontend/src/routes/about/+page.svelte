<div class="container">
	<div class="about-page">
		<h1>About Foldline</h1>

		<div class="card">
			<h2>Privacy-First Wearable Data Analysis</h2>
			<p>
				Foldline is a local-only desktop application for analyzing your wearable device data. It
				works with Garmin GDPR exports and local FIT files to provide insights into your health
				metrics.
			</p>
		</div>

		<div class="card privacy-card">
			<h2>Your Data, Your Machine</h2>
			<ul>
				<li>✓ All data processing happens locally on your computer</li>
				<li>✓ No data is sent to external servers or APIs</li>
				<li>✓ No Garmin Connect integration or OAuth</li>
				<li>✓ No analytics, tracking, or telemetry</li>
				<li>✓ No internet connection required after installation</li>
			</ul>
		</div>

		<div class="card">
			<h2>Features</h2>
			<ul>
				<li>Import Garmin GDPR "Export My Data" archives</li>
				<li>Scan local FIT file directories (e.g., Garmin Express folder)</li>
				<li>Visualize metrics: sleep, HRV, resting HR, stress, steps, and more</li>
				<li>Generate heatmaps and trend charts</li>
				<li>Analyze correlations between different metrics</li>
			</ul>
		</div>

		<div class="card">
			<h2>Technology Stack</h2>
			<ul>
				<li><strong>UI:</strong> SvelteKit + Tauri 2.0</li>
				<li><strong>Backend:</strong> Python (FastAPI)</li>
				<li><strong>Database:</strong> DuckDB / SQLite</li>
				<li><strong>Data Parsing:</strong> FIT file format support</li>
			</ul>
		</div>

		<div class="card">
			<h2>Version</h2>
			<p>Foldline v0.1.0</p>
			<p class="muted">Built with privacy and local-first principles</p>
		</div>
	</div>
</div>

<style>
	.about-page {
		max-width: 800px;
		margin: 0 auto;
		padding: calc(var(--spacing) * 2) 0;
	}

	.card {
		margin-bottom: var(--spacing);
	}

	.card h2 {
		color: var(--color-primary);
		margin-bottom: calc(var(--spacing) * 0.75);
	}

	.card p {
		color: var(--color-text-secondary);
		line-height: 1.6;
		margin-bottom: 8px;
	}

	.card p:last-child {
		margin-bottom: 0;
	}

	.card ul {
		list-style: none;
		padding: 0;
	}

	.card ul li {
		padding: 8px 0;
		color: var(--color-text-secondary);
		line-height: 1.6;
	}

	.privacy-card {
		background-color: rgba(76, 175, 80, 0.1);
		border-color: var(--color-success);
	}

	.privacy-card ul li {
		color: var(--color-success);
	}

	.muted {
		font-size: 0.9rem;
		font-style: italic;
	}

	strong {
		color: var(--color-text);
	}
</style>
