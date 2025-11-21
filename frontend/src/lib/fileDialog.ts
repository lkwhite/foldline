/**
 * File dialog utilities using Tauri's dialog plugin
 */

import { open } from '@tauri-apps/plugin-dialog';

/**
 * Open a file picker for selecting a Garmin GDPR export zip
 */
export async function selectGarminExport(): Promise<string | null> {
	const selected = await open({
		multiple: false,
		directory: false,
		filters: [
			{
				name: 'ZIP Files',
				extensions: ['zip']
			}
		],
		title: 'Select Garmin Export My Data ZIP'
	});

	return selected as string | null;
}

/**
 * Open a directory picker for selecting a FIT file folder
 */
export async function selectFitFolder(): Promise<string | null> {
	const selected = await open({
		multiple: false,
		directory: true,
		title: 'Select FIT Files Directory'
	});

	return selected as string | null;
}

/**
 * Open a directory picker for data root
 */
export async function selectDataRoot(): Promise<string | null> {
	const selected = await open({
		multiple: false,
		directory: true,
		title: 'Select Data Storage Directory'
	});

	return selected as string | null;
}
