// Add eel's exposed functions here
export interface Eel {
  expose(fn: () => void, name?: string): void;
}
