import { Link } from 'react-router-dom';

export default function PrimaryButton({
  children,
  to,
  href,
  onClick,
  type = 'button',
  variant = 'primary',
  className = '',
  disabled = false,
  ...props
}) {
  const baseClasses =
    'inline-flex items-center justify-center px-6 py-3 text-xs sm:text-sm font-semibold uppercase tracking-widest transition-all duration-200 rounded-xs focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer';

  const variants = {
    primary:
      'bg-theme-gold text-stone-950 hover:brightness-110 active:brightness-95 shadow-sm hover:shadow-md focus-visible:outline-[var(--color-gold)]',
    secondary:
      'bg-theme-elevated border border-theme text-theme-main hover:border-[var(--color-gold)] hover:text-theme-gold focus-visible:outline-[var(--color-gold)]',
    outline:
      'border border-theme-gold text-theme-gold hover:bg-theme-gold hover:text-stone-950 focus-visible:outline-[var(--color-gold)]',
    ghost:
      'text-theme-muted hover:text-theme-gold hover:bg-theme-elevated focus-visible:outline-[var(--color-gold)]',
  };

  const combinedClasses = `${baseClasses} ${variants[variant] || variants.primary} ${className}`;

  if (to) {
    return (
      <Link to={to} className={combinedClasses} {...props}>
        {children}
      </Link>
    );
  }

  if (href) {
    return (
      <a href={href} className={combinedClasses} {...props}>
        {children}
      </a>
    );
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={combinedClasses}
      {...props}
    >
      {children}
    </button>
  );
}
