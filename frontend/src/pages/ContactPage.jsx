import { usePageMeta } from '../hooks/usePageMeta';
import { useHotel } from '../hooks/useHotel';
import { useLanguage } from '../hooks/useLanguage';
import Container from '../components/common/Container';
import ContactForm from '../components/contact/ContactForm';
import CallbackForm from '../components/contact/CallbackForm';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

export default function ContactPage() {
  const { t } = useLanguage();
  usePageMeta({
    title: t('meta.contactTitle'),
    description: t('meta.contactDesc'),
    canonicalPath: '/contact',
  });
  const { hotelInfo } = useHotel();

  const hotelName = hotelInfo?.name || 'Coco Hotel';
  const phone = hotelInfo?.phone;
  const secondaryPhone = hotelInfo?.secondary_phone;
  const email = hotelInfo?.email;
  const address = hotelInfo?.address;
  const mapUrl = hotelInfo?.map_url;
  const checkInTime = hotelInfo?.check_in_time;
  const checkOutTime = hotelInfo?.check_out_time;

  return (
    <div className="flex flex-col bg-theme-main transition-colors duration-200">
      {/* 1. INTRO HEADING */}
      <section
        aria-label="Contact Coco Hotel Header"
        className="relative bg-theme-secondary text-theme-main py-20 sm:py-28 border-b border-theme overflow-hidden transition-colors duration-200"
      >
        <GoldWavePattern opacity={0.14} />
        <Container className="relative z-10 text-center">
          <RevealOnScroll variant="up">
            <span className="inline-block px-3.5 py-1 rounded-full text-[11px] font-bold uppercase tracking-[0.25em] text-[#fae28e] bg-[#dfba56]/15 border border-[#dfba56]/30 mb-4">
              {t('contact.conciergeSubtitle')}
            </span>
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-serif font-bold text-theme-main tracking-tight mb-4">
              {t('contact.title')}
            </h1>
            <p className="text-base sm:text-lg text-theme-muted font-light max-w-2xl mx-auto leading-relaxed">
              {t('contact.intro')}
            </p>
          </RevealOnScroll>
        </Container>
      </section>

      {/* 2. HOTEL CONTACT INFORMATION CARDS */}
      <section aria-label="Hotel Contact Details" className="relative py-16 sm:py-20 bg-theme-main border-b border-theme">
        <GoldWavePattern opacity={0.06} />
        <Container className="relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Phone */}
            <RevealOnScroll variant="up" delay={0}>
              <div className="p-7 bg-theme-surface border border-theme rounded-2xl flex flex-col justify-between hover:border-[#dfba56]/60 transition-all duration-300 shadow-xl hover:shadow-2xl h-full">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-[#dfba56]/10 border border-[#dfba56]/30 flex items-center justify-center text-[#dfba56] mb-4">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.75">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H3.75A2.25 2.25 0 001.5 4.5v2.25z" />
                    </svg>
                  </div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#fae28e] block mb-1">
                    {t('contact.telephone')}
                  </span>
                  <h2 className="text-lg font-serif font-bold text-theme-main mb-3">
                    {t('contact.directInquiries')}
                  </h2>
                  <div className="space-y-1.5 text-sm text-theme-muted">
                    {phone ? (
                      <p>
                        <a href={`tel:${phone}`} className="hover:text-[#fae28e] font-semibold transition-colors">
                          {phone}
                        </a>
                      </p>
                    ) : (
                      <p className="text-theme-subtle">{t('contact.frontDeskSupport')}</p>
                    )}
                    {secondaryPhone && (
                      <p className="text-xs text-theme-subtle">
                        <a href={`tel:${secondaryPhone}`} className="hover:text-[#fae28e] transition-colors">{secondaryPhone}</a>
                      </p>
                    )}
                  </div>
                </div>
                <p className="text-[11px] text-theme-subtle mt-6 pt-3 border-t border-theme">
                  {t('contact.frontDeskSupport')}
                </p>
              </div>
            </RevealOnScroll>

            {/* Email */}
            <RevealOnScroll variant="up" delay={80}>
              <div className="p-7 bg-theme-surface border border-theme rounded-2xl flex flex-col justify-between hover:border-[#dfba56]/60 transition-all duration-300 shadow-xl hover:shadow-2xl h-full">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-[#dfba56]/10 border border-[#dfba56]/30 flex items-center justify-center text-[#dfba56] mb-4">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.75">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                    </svg>
                  </div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#fae28e] block mb-1">
                    {t('contact.email')}
                  </span>
                  <h2 className="text-lg font-serif font-bold text-theme-main mb-3">
                    {t('contact.electronicCorresp')}
                  </h2>
                  <div className="text-sm text-theme-muted">
                    {email ? (
                      <p className="break-all">
                        <a href={`mailto:${email}`} className="hover:text-[#fae28e] font-semibold transition-colors">
                          {email}
                        </a>
                      </p>
                    ) : (
                      <p className="text-theme-subtle">{t('contact.promptReply')}</p>
                    )}
                  </div>
                </div>
                <p className="text-[11px] text-theme-subtle mt-6 pt-3 border-t border-theme">
                  {t('contact.promptReply')}
                </p>
              </div>
            </RevealOnScroll>

            {/* Address */}
            <RevealOnScroll variant="up" delay={160}>
              <div className="p-7 bg-theme-surface border border-theme rounded-2xl flex flex-col justify-between hover:border-[#dfba56]/60 transition-all duration-300 shadow-xl hover:shadow-2xl h-full">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-[#dfba56]/10 border border-[#dfba56]/30 flex items-center justify-center text-[#dfba56] mb-4">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.75">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                    </svg>
                  </div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#fae28e] block mb-1">
                    {t('contact.location')}
                  </span>
                  <h2 className="text-lg font-serif font-bold text-theme-main mb-3">
                    {t('contact.physicalAddress')}
                  </h2>
                  <div className="text-sm text-theme-muted leading-relaxed">
                    <a
                      href={mapUrl || "https://yandex.uz/maps/-/CPwOM2O3"}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-amber-500 transition-colors block"
                      title="Xaritada ochish"
                    >
                      {address || '156 Bogibuston Street, Tashkent 100022, Uzbekistan'}
                    </a>
                  </div>
                </div>
                <div className="mt-6 pt-3 border-t border-theme">
                  <a
                    href={mapUrl || "https://yandex.uz/maps/-/CPwOM2O3"}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-500/15 border border-amber-400/60 text-amber-500 hover:bg-amber-500 hover:text-stone-950 text-xs font-bold uppercase tracking-wider transition-all shadow-xs"
                  >
                    <span>📍</span>
                    <span>{t('contact.openInMaps') || 'Xaritada ochish (Yandex Maps)'} ↗</span>
                  </a>
                </div>
              </div>
            </RevealOnScroll>

            {/* Check-In / Check-Out */}
            <RevealOnScroll variant="up" delay={240}>
              <div className="p-7 bg-theme-surface border border-theme rounded-2xl flex flex-col justify-between hover:border-[#dfba56]/60 transition-all duration-300 shadow-xl hover:shadow-2xl h-full">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-[#dfba56]/10 border border-[#dfba56]/30 flex items-center justify-center text-[#dfba56] mb-4">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.75">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#fae28e] block mb-1">
                    {t('contact.hoursTiming')}
                  </span>
                  <h2 className="text-lg font-serif font-bold text-theme-main mb-3">
                    {t('contact.staySchedule')}
                  </h2>
                  <div className="space-y-2 text-sm text-theme-muted">
                    <div>
                      <span className="text-[11px] text-theme-subtle block uppercase tracking-wider">{t('booking.checkIn')}</span>
                      <span className="font-semibold text-theme-main">
                        {checkInTime || 'From 14:00'}
                      </span>
                    </div>
                    <div>
                      <span className="text-[11px] text-theme-subtle block uppercase tracking-wider">{t('booking.checkOut')}</span>
                      <span className="font-semibold text-theme-main">
                        {checkOutTime || 'Until 12:00'}
                      </span>
                    </div>
                  </div>
                </div>
                <p className="text-[11px] text-theme-subtle mt-6 pt-3 border-t border-theme">
                  {t('contact.reception247')}
                </p>
              </div>
            </RevealOnScroll>
          </div>
        </Container>
      </section>

      {/* 3 & 4. GUEST FORMS (CONTACT MESSAGE & CALLBACK REQUEST) */}
      <section aria-label="Guest Inquiries and Callback Requests" className="relative py-16 sm:py-24 bg-theme-main">
        <GoldWavePattern opacity={0.07} />
        <Container className="relative z-10">
          <RevealOnScroll variant="up">
            <div className="text-center max-w-2xl mx-auto mb-12 sm:mb-16">
              <span className="inline-block px-3.5 py-1 rounded-full text-[11px] font-bold uppercase tracking-[0.25em] text-[#fae28e] bg-[#dfba56]/15 border border-[#dfba56]/30 mb-3">
                {t('contact.getInTouch')}
              </span>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-serif font-bold text-theme-main tracking-tight mb-4">
                {t('contact.howMayWeHelp')}
              </h2>
              <p className="text-sm sm:text-base text-theme-muted leading-relaxed font-light">
                {t('contact.howMayWeHelpDesc')}
              </p>
            </div>
          </RevealOnScroll>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-start">
            {/* Contact Message Form */}
            <RevealOnScroll variant="left">
              <ContactForm />
            </RevealOnScroll>

            {/* Callback Request Form */}
            <RevealOnScroll variant="right" delay={150}>
              <CallbackForm />
            </RevealOnScroll>
          </div>
        </Container>
      </section>

      {/* 5. LOCATION / DIRECTIONS AREA */}
      {(address || mapUrl) && (
        <section
          aria-label="Location and Directions"
          className="relative py-16 sm:py-20 bg-theme-secondary text-theme-main border-t border-theme overflow-hidden transition-colors duration-200"
        >
          <GoldWavePattern opacity={0.1} />
          <Container className="relative z-10">
            <RevealOnScroll variant="up">
              <div className="max-w-3xl mx-auto text-center space-y-6">
                <span className="text-xs font-bold uppercase tracking-[0.2em] text-[#fae28e] block">
                  {t('contact.findingHotel')} {hotelName}
                </span>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-theme-main">
                  {t('contact.directionsTitle')}
                </h2>
                {address && (
                  <p className="text-theme-muted text-base leading-relaxed">
                    {address}
                  </p>
                )}
                <p className="text-sm text-theme-muted leading-relaxed max-w-xl mx-auto font-light">
                  {t('contact.directionsDesc')}
                </p>
                {mapUrl && (
                  <div className="pt-2">
                    <a
                      href={mapUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-wider bg-gold-metallic text-stone-950 rounded-xl hover:shadow-lg hover:shadow-[#dfba56]/25 active:scale-95 transition-all"
                    >
                      {t('contact.viewInteractiveMap')} &rarr;
                    </a>
                  </div>
                )}
              </div>
            </RevealOnScroll>
          </Container>
        </section>
      )}
    </div>
  );
}
