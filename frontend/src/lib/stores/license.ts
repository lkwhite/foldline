import { writable } from 'svelte/store';

export interface LicenseState {
  isActivated: boolean;
  licenseKey: string | null;
  activatedAt: string | null;
}

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
  };
}

export const license = createLicenseStore();
