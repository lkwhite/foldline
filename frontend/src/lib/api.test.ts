/**
 * Tests for API client module.
 *
 * Tests:
 * - Backend initialization
 * - URL construction
 * - GET and POST requests
 * - Error handling
 * - Health check
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
	initBackend,
	getBackendUrl,
	apiGet,
	apiPost,
	checkBackendHealth
} from './api';

// Mock Tauri's invoke function
vi.mock('@tauri-apps/api/core', () => ({
	invoke: vi.fn()
}));

import { invoke } from '@tauri-apps/api/core';

describe('API Client', () => {
	beforeEach(() => {
		// Reset module state between tests
		vi.clearAllMocks();

		// Reset the global fetch mock
		global.fetch = vi.fn();
	});

	afterEach(() => {
		vi.restoreAllMocks();
	});

	describe('initBackend', () => {
		it('should start backend and return port', async () => {
			const mockPort = 8500;
			vi.mocked(invoke).mockResolvedValue(mockPort);

			const port = await initBackend();

			expect(port).toBe(mockPort);
			expect(invoke).toHaveBeenCalledWith('start_backend');
		});

		it('should cache backend port on subsequent calls', async () => {
			const mockPort = 8500;
			vi.mocked(invoke).mockResolvedValue(mockPort);

			const port1 = await initBackend();
			const port2 = await initBackend();

			expect(port1).toBe(mockPort);
			expect(port2).toBe(mockPort);
			// Should only invoke once due to caching
			expect(invoke).toHaveBeenCalledTimes(1);
		});

		it('should throw error if backend fails to start', async () => {
			vi.mocked(invoke).mockRejectedValue(new Error('Failed to start'));

			await expect(initBackend()).rejects.toThrow('Failed to start');
		});

		it('should log success message on start', async () => {
			const consoleSpy = vi.spyOn(console, 'log');
			const mockPort = 8500;
			vi.mocked(invoke).mockResolvedValue(mockPort);

			await initBackend();

			expect(consoleSpy).toHaveBeenCalledWith(
				expect.stringContaining('Backend started on port 8500')
			);
		});

		it('should log error message on failure', async () => {
			const consoleSpy = vi.spyOn(console, 'error');
			const error = new Error('Connection failed');
			vi.mocked(invoke).mockRejectedValue(error);

			await expect(initBackend()).rejects.toThrow();

			expect(consoleSpy).toHaveBeenCalledWith(
				'Failed to start backend:',
				error
			);
		});
	});

	describe('getBackendUrl', () => {
		it('should return correct URL when backend is initialized', async () => {
			const mockPort = 8500;
			vi.mocked(invoke).mockResolvedValue(mockPort);

			await initBackend();
			const url = getBackendUrl();

			expect(url).toBe('http://127.0.0.1:8500');
		});

		it('should throw error when backend not initialized', () => {
			expect(() => getBackendUrl()).toThrow('Backend not initialized');
		});

		it('should use 127.0.0.1 for security', async () => {
			const mockPort = 8000;
			vi.mocked(invoke).mockResolvedValue(mockPort);

			await initBackend();
			const url = getBackendUrl();

			expect(url).toContain('127.0.0.1');
			expect(url).not.toContain('localhost'); // Should use IP
		});
	});

	describe('apiGet', () => {
		beforeEach(async () => {
			// Initialize backend for GET/POST tests
			vi.mocked(invoke).mockResolvedValue(8500);
			await initBackend();
		});

		it('should make GET request to correct URL', async () => {
			const mockData = { result: 'success' };
			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => mockData
			} as Response);

			await apiGet('/status');

			expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8500/status');
		});

		it('should return parsed JSON response', async () => {
			const mockData = { foo: 'bar', count: 42 };
			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => mockData
			} as Response);

			const result = await apiGet('/test');

			expect(result).toEqual(mockData);
		});

		it('should throw error on HTTP error status', async () => {
			vi.mocked(global.fetch).mockResolvedValue({
				ok: false,
				statusText: 'Not Found'
			} as Response);

			await expect(apiGet('/notfound')).rejects.toThrow('API error: Not Found');
		});

		it('should handle network errors', async () => {
			vi.mocked(global.fetch).mockRejectedValue(new Error('Network error'));

			await expect(apiGet('/status')).rejects.toThrow('Network error');
		});

		it('should handle endpoints with query parameters', async () => {
			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => ({})
			} as Response);

			await apiGet('/metrics/heatmap?metric=sleep&start_date=2024-01-01');

			expect(global.fetch).toHaveBeenCalledWith(
				'http://127.0.0.1:8500/metrics/heatmap?metric=sleep&start_date=2024-01-01'
			);
		});
	});

	describe('apiPost', () => {
		beforeEach(async () => {
			vi.mocked(invoke).mockResolvedValue(8500);
			await initBackend();
		});

		it('should make POST request with JSON body', async () => {
			const postData = { folder_path: '/test/path' };
			const mockResponse = { success: true };

			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => mockResponse
			} as Response);

			await apiPost('/import/fit-folder', postData);

			expect(global.fetch).toHaveBeenCalledWith(
				'http://127.0.0.1:8500/import/fit-folder',
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(postData)
				}
			);
		});

		it('should return parsed JSON response', async () => {
			const mockResponse = { success: true, message: 'Imported' };
			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => mockResponse
			} as Response);

			const result = await apiPost('/test', { data: 'test' });

			expect(result).toEqual(mockResponse);
		});

		it('should throw error on HTTP error status', async () => {
			vi.mocked(global.fetch).mockResolvedValue({
				ok: false,
				statusText: 'Bad Request'
			} as Response);

			await expect(apiPost('/test', {})).rejects.toThrow('API error: Bad Request');
		});

		it('should handle empty request body', async () => {
			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => ({})
			} as Response);

			await apiPost('/test', {});

			expect(global.fetch).toHaveBeenCalledWith(
				expect.any(String),
				expect.objectContaining({
					body: '{}'
				})
			);
		});

		it('should set Content-Type header', async () => {
			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => ({})
			} as Response);

			await apiPost('/test', { data: 'test' });

			const callArgs = vi.mocked(global.fetch).mock.calls[0];
			const options = callArgs[1] as RequestInit;

			expect(options.headers).toEqual({
				'Content-Type': 'application/json'
			});
		});
	});

	describe('checkBackendHealth', () => {
		it('should return false when backend not initialized', async () => {
			const health = await checkBackendHealth();

			expect(health).toBe(false);
		});

		it('should invoke health check command with port', async () => {
			const mockPort = 8500;
			vi.mocked(invoke).mockResolvedValue(mockPort);
			await initBackend();

			vi.mocked(invoke).mockResolvedValue(true);
			const health = await checkBackendHealth();

			expect(health).toBe(true);
			expect(invoke).toHaveBeenCalledWith('check_backend_health', { port: mockPort });
		});

		it('should return false on health check error', async () => {
			const mockPort = 8500;
			vi.mocked(invoke)
				.mockResolvedValueOnce(mockPort)  // initBackend
				.mockRejectedValueOnce(new Error('Health check failed'));  // checkBackendHealth

			await initBackend();
			const health = await checkBackendHealth();

			expect(health).toBe(false);
		});

		it('should handle connection timeout gracefully', async () => {
			const mockPort = 8500;
			vi.mocked(invoke)
				.mockResolvedValueOnce(mockPort)
				.mockImplementationOnce(() =>
					new Promise((_, reject) =>
						setTimeout(() => reject(new Error('Timeout')), 100)
					)
				);

			await initBackend();
			const health = await checkBackendHealth();

			expect(health).toBe(false);
		});
	});

	describe('Error Handling', () => {
		it('should handle 404 errors', async () => {
			vi.mocked(invoke).mockResolvedValue(8500);
			await initBackend();

			vi.mocked(global.fetch).mockResolvedValue({
				ok: false,
				statusText: 'Not Found'
			} as Response);

			await expect(apiGet('/nonexistent')).rejects.toThrow('Not Found');
		});

		it('should handle 500 errors', async () => {
			vi.mocked(invoke).mockResolvedValue(8500);
			await initBackend();

			vi.mocked(global.fetch).mockResolvedValue({
				ok: false,
				statusText: 'Internal Server Error'
			} as Response);

			await expect(apiGet('/error')).rejects.toThrow('Internal Server Error');
		});

		it('should handle malformed JSON responses', async () => {
			vi.mocked(invoke).mockResolvedValue(8500);
			await initBackend();

			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => {
					throw new Error('Invalid JSON');
				}
			} as Response);

			await expect(apiGet('/test')).rejects.toThrow('Invalid JSON');
		});
	});

	describe('Integration Scenarios', () => {
		it('should handle full workflow: init -> get -> post', async () => {
			// Initialize
			vi.mocked(invoke).mockResolvedValue(8500);
			await initBackend();

			// GET request
			vi.mocked(global.fetch).mockResolvedValueOnce({
				ok: true,
				json: async () => ({ status: 'ok' })
			} as Response);
			const status = await apiGet('/status');
			expect(status).toEqual({ status: 'ok' });

			// POST request
			vi.mocked(global.fetch).mockResolvedValueOnce({
				ok: true,
				json: async () => ({ success: true })
			} as Response);
			const result = await apiPost('/import/fit-folder', { folder_path: '/test' });
			expect(result).toEqual({ success: true });
		});

		it('should maintain backend URL across multiple requests', async () => {
			vi.mocked(invoke).mockResolvedValue(8500);
			await initBackend();

			vi.mocked(global.fetch).mockResolvedValue({
				ok: true,
				json: async () => ({})
			} as Response);

			await apiGet('/endpoint1');
			await apiGet('/endpoint2');
			await apiPost('/endpoint3', {});

			const calls = vi.mocked(global.fetch).mock.calls;
			expect(calls[0][0]).toContain('127.0.0.1:8500');
			expect(calls[1][0]).toContain('127.0.0.1:8500');
			expect(calls[2][0]).toContain('127.0.0.1:8500');
		});
	});
});
