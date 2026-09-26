export function formatPrice(amount, currency = 'USD') {
  if (amount == null) return '';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

export function formatUZSPrice(amount, lang = 'uz') {
  if (amount == null || amount === '') return '';
  const num = typeof amount === 'number' ? amount : parseFloat(amount);
  if (isNaN(num)) return `${amount} UZS`;
  const formatted = new Intl.NumberFormat('ru-RU').format(Math.round(num));
  if (lang === 'uz') return `${formatted} so‘m`;
  if (lang === 'ru') return `${formatted} сум`;
  return `${formatted} UZS`;
}

export function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(/^\d{4}-\d{2}-\d{2}$/.test(dateString) ? `${dateString}T00:00:00` : dateString);
  if (Number.isNaN(date.getTime())) return '';
  const language = typeof document === 'undefined' ? 'en' : document.documentElement.lang || 'en';
  return new Intl.DateTimeFormat(language, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date);
}
