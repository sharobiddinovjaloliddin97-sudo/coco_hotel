import { useState } from 'react';
import { createCallbackRequest } from '../../api/guestRequests';
import { useLanguage } from '../../hooks/useLanguage';

export default function CallbackForm() {
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    full_name: '',
    phone: '',
    preferred_time: '',
    message: '',
    website: '', // anti-spam honeypot
  });

  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [fieldErrors, setFieldErrors] = useState({});
  const [generalError, setGeneralError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (fieldErrors[name]) {
      setFieldErrors((prev) => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
    if (generalError) {
      setGeneralError('');
    }
  };

  const validate = () => {
    const errors = {};
    if (!formData.full_name.trim()) {
      errors.full_name = t('contact.nameRequired');
    }
    if (!formData.phone.trim()) {
      errors.phone = t('contact.phoneRequired');
    }
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (submitting) return;

    setGeneralError('');
    setFieldErrors({});

    const clientErrors = validate();
    if (Object.keys(clientErrors).length > 0) {
      setFieldErrors(clientErrors);
      return;
    }

    setSubmitting(true);

    try {
      const payload = {
        full_name: formData.full_name.trim(),
        phone: formData.phone.trim(),
        preferred_time: formData.preferred_time.trim(),
        message: formData.message.trim(),
        website: formData.website || '',
      };

      const response = await createCallbackRequest(payload);

      if (response.status === 201 || response.status === 200) {
        setSuccess(true);
        setSuccessMessage(
          t('contact.callbackSuccess')
        );
        setFormData({
          full_name: '',
          phone: '',
          preferred_time: '',
          message: '',
          website: '',
        });
      }
    } catch (err) {
      const status = err.response?.status;
      const data = err.response?.data;

      if (status === 400 && data) {
        const backendErrors = {};
        if (typeof data === 'object') {
          Object.keys(data).forEach((field) => {
            const errVal = data[field];
            backendErrors[field] = Array.isArray(errVal) ? errVal.join(' ') : String(errVal);
          });
        }
        setFieldErrors(backendErrors);
        if (data.detail) {
          setGeneralError(data.detail);
        }
      } else if (status === 429) {
        setGeneralError(t('contact.rateLimitError'));
      } else {
        setGeneralError(t('contact.submitError'));
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleReset = () => {
    setSuccess(false);
    setSuccessMessage('');
    setGeneralError('');
    setFieldErrors({});
  };

  return (
    <div className="bg-theme-surface border border-theme rounded-2xl p-6 sm:p-8 shadow-2xl transition-colors duration-200">
      <div className="mb-6">
        <h2 className="text-xl font-serif font-bold text-theme-main mb-1">
          {t('contact.requestCallback')}
        </h2>
        <p className="text-xs text-theme-muted">
          {t('contact.callbackDesc')}
        </p>
      </div>

      {success ? (
        <div
          role="status"
          aria-live="polite"
          className="p-6 bg-theme-elevated border border-theme rounded-xs text-center space-y-4"
        >
          <div className="w-12 h-12 mx-auto rounded-full bg-theme-gold/10 text-theme-gold flex items-center justify-center border border-theme-gold">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-serif font-bold text-theme-main">
              {t('contact.requestReceivedTitle')}
            </h3>
            <p className="text-xs sm:text-sm text-theme-muted leading-relaxed max-w-md mx-auto">
              {successMessage}
            </p>
          </div>
          <button
            type="button"
            onClick={handleReset}
            className="inline-flex items-center justify-center px-4 py-2 text-xs font-semibold uppercase tracking-wider text-theme-gold hover:underline cursor-pointer transition-colors"
          >
            {t('contact.submitAnother')}
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} noValidate className="space-y-4">
          {/* Honeypot field */}
          <div style={{ display: 'none' }} aria-hidden="true">
            <label htmlFor="callback_website">Website</label>
            <input
              id="callback_website"
              type="text"
              name="website"
              value={formData.website}
              onChange={handleChange}
              tabIndex="-1"
              autoComplete="off"
            />
          </div>

          {generalError && (
            <div
              role="alert"
              className="p-3 bg-rose-950/20 border border-rose-500/50 text-xs text-rose-500 rounded-xs"
            >
              {generalError}
            </div>
          )}

          {/* Full Name */}
          <div>
            <label
              htmlFor="callback_full_name"
              className="block text-xs font-semibold uppercase tracking-wider text-theme-gold mb-1"
            >
              {t('contact.fullName')} <span className="text-theme-gold">*</span>
            </label>
            <input
              id="callback_full_name"
              type="text"
              name="full_name"
              autoComplete="name"
              value={formData.full_name}
              onChange={handleChange}
              placeholder="e.g. John Doe"
              disabled={submitting}
              className={`w-full px-3.5 py-2.5 text-sm bg-theme-input border ${
                fieldErrors.full_name ? 'border-rose-500' : 'border-theme focus:border-[var(--color-gold)]'
              } text-theme-main placeholder:text-theme-subtle rounded-xs focus:outline-none transition-colors disabled:opacity-50`}
            />
            {fieldErrors.full_name && (
              <p role="alert" className="mt-1 text-xs text-rose-500">
                {fieldErrors.full_name}
              </p>
            )}
          </div>

          {/* Phone Number */}
          <div>
            <label
              htmlFor="callback_phone"
              className="block text-xs font-semibold uppercase tracking-wider text-theme-gold mb-1"
            >
              {t('contact.phone')} <span className="text-theme-gold">*</span>
            </label>
            <input
              id="callback_phone"
              type="tel"
              name="phone"
              autoComplete="tel"
              value={formData.phone}
              onChange={handleChange}
              placeholder="e.g. +998 90 123 4567"
              disabled={submitting}
              className={`w-full px-3.5 py-2.5 text-sm bg-theme-input border ${
                fieldErrors.phone ? 'border-rose-500' : 'border-theme focus:border-[var(--color-gold)]'
              } text-theme-main placeholder:text-theme-subtle rounded-xs focus:outline-none transition-colors disabled:opacity-50`}
            />
            {fieldErrors.phone && (
              <p role="alert" className="mt-1 text-xs text-rose-500">
                {fieldErrors.phone}
              </p>
            )}
          </div>

          {/* Preferred Time */}
          <div>
            <label
              htmlFor="callback_preferred_time"
              className="block text-xs font-semibold uppercase tracking-wider text-theme-gold mb-1"
            >
              {t('contact.preferredTime')} <span className="text-theme-subtle font-normal">({t('contact.optional')})</span>
            </label>
            <input
              id="callback_preferred_time"
              type="text"
              name="preferred_time"
              value={formData.preferred_time}
              onChange={handleChange}
              placeholder="e.g. Morning 10:00 – 12:00, or ASAP"
              disabled={submitting}
              className="w-full px-3.5 py-2.5 text-sm bg-theme-input border border-theme text-theme-main placeholder:text-theme-subtle rounded-xs focus:border-[var(--color-gold)] focus:outline-none transition-colors disabled:opacity-50"
            />
          </div>

          {/* Message / Notes */}
          <div>
            <label
              htmlFor="callback_message"
              className="block text-xs font-semibold uppercase tracking-wider text-theme-gold mb-1"
            >
              {t('contact.inquiryNote')} <span className="text-theme-subtle font-normal">({t('contact.optional')})</span>
            </label>
            <textarea
              id="callback_message"
              name="message"
              rows={3}
              value={formData.message}
              onChange={handleChange}
              placeholder="Briefly describe what you would like to discuss..."
              disabled={submitting}
              className="w-full px-3.5 py-2.5 text-sm bg-theme-input border border-theme text-theme-main placeholder:text-theme-subtle rounded-xs focus:border-[var(--color-gold)] focus:outline-none transition-colors disabled:opacity-50 resize-y"
            />
          </div>

          {/* Submit Button */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={submitting}
              className="w-full inline-flex items-center justify-center px-6 py-3.5 text-xs font-bold uppercase tracking-wider bg-gold-metallic text-stone-950 rounded-xl hover:shadow-lg hover:shadow-[#dfba56]/25 disabled:opacity-50 transition-all cursor-pointer focus-visible:outline-2 focus-visible:outline-[#dfba56]"
            >
              {submitting ? (
                <span className="inline-flex items-center gap-2">
                  <svg className="animate-spin w-4 h-4 text-stone-950" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  {t('contact.submitting')}
                </span>
              ) : (
                t('contact.submitCallback')
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
