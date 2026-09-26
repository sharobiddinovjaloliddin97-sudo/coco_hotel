import { useLanguage } from '../../hooks/useLanguage';

export default function LoadingState({ message, className = '' }) {
  const { t } = useLanguage();
  const displayMessage = message || t('common.loading');

  return (
    <div
      role="status"
      aria-live="polite"
      className={`flex flex-col items-center justify-center p-8 text-theme-muted ${className}`}
    >
      <div
        className="w-8 h-8 border-2 border-theme border-t-[var(--color-gold)] rounded-full animate-spin mb-3"
        aria-hidden="true"
      />
      <p className="text-sm font-normal text-theme-muted">{displayMessage}</p>
      <span className="sr-only">{displayMessage}</span>
    </div>
  );
}
