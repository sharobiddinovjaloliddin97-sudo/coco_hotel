import { usePageMeta } from './usePageMeta';

/**
 * Backward-compatible hook delegating to centralized usePageMeta.
 */
export function useDocumentTitle(title) {
  usePageMeta({ title });
}

export default useDocumentTitle;
