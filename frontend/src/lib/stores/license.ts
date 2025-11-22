import { writable, derived } from 'svelte/store';

export interface LicenseState {
  isActivated: boolean;
  licenseKey: string | null;
  activatedAt: string | null;
}

export type PremiumFeature =
  | 'unlimited_import'        // Free: Garmin only, Premium: all sources
  | 'full_history'            // Free: 30 days, Premium: unlimited
  | 'correlation_analysis'    // Premium only
  | 'data_export'             // Premium only
  | 'advanced_filters'        // Premium only
  | 'custom_date_ranges'      // Premium only
  | 'multi_metric_heatmaps';  // Free: single metric, Premium: multiple

const STORAGE_KEY = 'foldline_license';

function createLicenseStore() {
  // Initialize from localStorage
  const storedLicense = typeof window !== 'undefined'
    ? localStorage.getItem(STORAGE_KEY)
    : null;

  const initialState: LicenseState = storedLicense
    ? JSON.parse(storedLicense)
    : {
        isActivated: false,
        licenseKey: null,
        activatedAt: null,
      };

  const { subscribe, set, update } = writable<LicenseState>(initialState);

  return {
    subscribe,
    activate: (key: string) => {
      const newState: LicenseState = {
        isActivated: true,
        licenseKey: key,
        activatedAt: new Date().toISOString(),
      };
      set(newState);
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newState));
      }
    },
    deactivate: () => {
      const newState: LicenseState = {
        isActivated: false,
        licenseKey: null,
        activatedAt: null,
      };
      set(newState);
      if (typeof window !== 'undefined') {
        localStorage.removeItem(STORAGE_KEY);
      }
    },
    getMaskedKey: (key: string): string => {
      if (!key || key.length < 4) return '****';
      const lastFour = key.slice(-4);
      const masked = '••••-••••-••••-' + lastFour;
      return masked;
    },
    hasFeature: (feature: PremiumFeature, state: LicenseState): boolean => {
      // Premium features require activation
      return state.isActivated;
    },
  };
}

export const license = createLicenseStore();

// Derived store for premium status
export const isPremium = derived(license, ($license) => $license.isActivated);

// Helper to check if a specific feature is available
export const hasFeature = (feature: PremiumFeature) => {
  return derived(license, ($license) => license.hasFeature(feature, $license));
};
