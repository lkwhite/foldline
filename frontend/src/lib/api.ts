/**
 * API client for communicating with the local Python backend
 */

import { invoke } from '@tauri-apps/api/core';

let backendPort: number | null = null;

/**
 * Initialize the backend connection
 */
export async function initBackend(): Promise<number> {
	if (backendPort !== null) {
		return backendPort;
	}

	try {
		// Start the backend and get the port
		backendPort = await invoke<number>('start_backend');
		console.log(`✓ Backend started on port ${backendPort}`);
		return backendPort;
	} catch (error) {
		console.error('Failed to start backend:', error);
		throw error;
	}
}

/**
 * Get the backend URL
 */
export function getBackendUrl(): string {
	if (backendPort === null) {
		throw new Error('Backend not initialized');
	}
	return `http://127.0.0.1:${backendPort}`;
}

/**
 * Make a GET request to the backend
 */
export async function apiGet<T>(endpoint: string): Promise<T> {
	const url = `${getBackendUrl()}${endpoint}`;
	const response = await fetch(url);

	if (!response.ok) {
		throw new Error(`API error: ${response.statusText}`);
	}

	return response.json();
}

/**
 * Make a POST request to the backend
 */
export async function apiPost<T>(endpoint: string, data: any): Promise<T> {
	const url = `${getBackendUrl()}${endpoint}`;
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	});

	if (!response.ok) {
		throw new Error(`API error: ${response.statusText}`);
	}

	return response.json();
}

/**
 * Check backend health
 */
export async function checkBackendHealth(): Promise<boolean> {
	if (backendPort === null) {
		return false;
	}

	try {
		return await invoke<boolean>('check_backend_health', { port: backendPort });
	} catch {
		return false;
	}
}
