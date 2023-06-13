// See https://kit.svelte.dev/docs/types#app

import type { Eel } from '$types/eel';

// for information about these interfaces
declare global {
  namespace App {
    // interface Error {}
    // interface Locals {}
    // interface PageData {}
    // interface Platform {}
  }

  interface Window {
    eel: Eel;
  }

  const eel: Eel;
}

export {};
