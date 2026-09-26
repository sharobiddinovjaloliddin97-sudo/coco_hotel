import { useLanguage } from '../../hooks/useLanguage';

export default function ErrorState({
  title,
  message,
  onRetry,
  className = '',
}) {
  const { t } = useLanguage();
  const displayTitle = title || t('common.errorTitle');
  const displayMessage = message || t('common.errorMessage');

  return (
    <div
      role="alert"
      className={`p-6 border border-theme bg-theme-elevated rounded-xs text-center ${className}`}
    >
      <h3 className="text-base font-serif font-semibold text-theme-main mb-1">{displayTitle}</h3>
      <p className="text-sm text-theme-muted mb-4">{displayMessage}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center px-4 py-2 text-xs font-semibold uppercase tracking-wider text-theme-gold bg-theme-surface border border-theme-gold rounded-xs hover:bg-theme-gold hover:text-stone-950 transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] cursor-pointer"
        >
          {t('common.retry')}
        </button>
      )}
    </div>
  );
}
