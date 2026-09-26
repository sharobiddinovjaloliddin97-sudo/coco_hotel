import { Link } from 'react-router-dom';
import { usePageMeta } from '../hooks/usePageMeta';
import { useLanguage } from '../hooks/useLanguage';
import Container from '../components/common/Container';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

export default function NotFoundPage() {
  const { t } = useLanguage();
  usePageMeta({
    title: '404',
    description: t('notFound.desc'),
    canonicalPath: '/404',
  });

  return (
    <div className="relative py-24 sm:py-36 bg-theme-main min-h-[70vh] flex items-center overflow-hidden transition-colors duration-200">
      <GoldWavePattern opacity={0.12} />
      <Container className="relative z-10 text-center">
        <RevealOnScroll variant="up">
          <span className="inline-block px-3.5 py-1 rounded-full text-xs font-bold uppercase tracking-[0.25em] text-[#fae28e] bg-[#dfba56]/15 border border-[#dfba56]/30 mb-4">
            404 — Sanctuary Lost
          </span>
          <h1 className="text-5xl sm:text-7xl lg:text-8xl font-serif font-bold text-theme-main tracking-tight mb-4">
            {t('notFound.title')}
          </h1>
          <p className="text-base sm:text-lg text-theme-muted max-w-md mx-auto mb-10 font-light leading-relaxed">
            {t('notFound.desc')}
          </p>
          <div>
            <Link
              to="/"
              className="inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic text-stone-950 rounded-xl hover:shadow-lg hover:shadow-[#dfba56]/25 active:scale-95 transition-all"
            >
              {t('notFound.returnHome')}
            </Link>
          </div>
        </RevealOnScroll>
      </Container>
    </div>
  );
}
