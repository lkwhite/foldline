<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
</script>

<div class="app">
	<nav>
		<div class="nav-content">
			<h1 class="logo">Foldline</h1>
			<div class="nav-links">
				<a href="/" class:active={$page.url.pathname === '/'}>Setup</a>
				<a href="/dashboard" class:active={$page.url.pathname === '/dashboard'}>Dashboard</a>
				<a href="/heatmaps" class:active={$page.url.pathname === '/heatmaps'}>Heatmaps</a>
				<a href="/trends" class:active={$page.url.pathname === '/trends'}>Trends</a>
				<a href="/correlation" class:active={$page.url.pathname === '/correlation'}>Correlation</a>
				<a href="/settings" class:active={$page.url.pathname === '/settings'}>Settings</a>
				<a href="/about" class:active={$page.url.pathname === '/about'}>About</a>
			</div>
		</div>
	</nav>

	<main>
		<slot />
	</main>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	nav {
		background-color: var(--color-bg-secondary);
		border-bottom: 1px solid var(--color-border);
		padding: 0 var(--spacing);
	}

	.nav-content {
		max-width: 1200px;
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 60px;
	}

	.logo {
		font-size: 1.5rem;
		font-weight: 700;
		margin: 0;
		color: var(--color-primary);
	}

	.nav-links {
		display: flex;
		gap: calc(var(--spacing) * 1.5);
	}

	.nav-links a {
		color: var(--color-text-secondary);
		text-decoration: none;
		font-weight: 500;
		transition: color 0.2s;
	}

	.nav-links a:hover {
		color: var(--color-text);
	}

	.nav-links a.active {
		color: var(--color-primary);
	}

	main {
		flex: 1;
	}
</style>
