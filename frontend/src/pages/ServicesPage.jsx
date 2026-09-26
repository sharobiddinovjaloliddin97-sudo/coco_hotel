import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { usePageMeta } from '../hooks/usePageMeta';
import { useLanguage } from '../hooks/useLanguage';
import { getServices } from '../api/hotel';
import Container from '../components/common/Container';
import SectionTitle from '../components/common/SectionTitle';
import ServiceIcon from '../components/common/ServiceIcon';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

export default function ServicesPage() {
  const { language, t } = useLanguage();
  usePageMeta({
    title: t('meta.servicesTitle'),
    description: t('meta.servicesDesc'),
    canonicalPath: '/services',
  });

  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const handleRetry = () => {
    setLoading(true);
    setError(false);
    getServices()
      .then((data) => {
        setServices(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  };

  useEffect(() => {
    let isMounted = true;
    getServices()
      .then((data) => {
        if (isMounted) {
          setServices(Array.isArray(data) ? data : []);
          setLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) {
          setError(true);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [language]);

  const amenityCategories = [
    {
      titleRu: "Ванная комната",
      titleUz: "Hammom qulayliklari",
      titleEn: "Bathroom Amenities",
      icon: "droplet",
      items: [
        { ru: "Собственная ванная комната", uz: "Shaxsiy hammom", en: "Private bathroom" },
        { ru: "Бесплатные туалетно-косметические принадлежности", uz: "Bepul gigiyena vositalari", en: "Free toiletries" },
        { ru: "Фен", uz: "Soch quritgich (Fen)", en: "Hairdryer" },
        { ru: "Тапочки и полотенца", uz: "Yumshoq shippaklar va sochiqlar", en: "Slippers and towels" },
        { ru: "Ванна или тропический душ", uz: "Vanna yoki tropik dush", en: "Bath or rain shower" },
        { ru: "Биде и туалет", uz: "Bide va hojatxona", en: "Bidet & toilet" },
      ],
    },
    {
      titleRu: "В номере и технологии",
      titleUz: "Xona ichidagi qulayliklar",
      titleEn: "In-Room & Technology",
      icon: "tv",
      items: [
        { ru: "Smart TV с плоским экраном (Кабельные каналы)", uz: "Yassi ekranli Smart TV (Kabel kanallari)", en: "Flat-screen Smart TV" },
        { ru: "Индивидуальный кондиционер и отопление", uz: "Individual konditsioner va isitish tizimi", en: "Climate control & heating" },
        { ru: "Звукоизолированные номера", uz: "Ovoz o'tkazmaydigan xonalar", en: "Soundproof rooms" },
        { ru: "Удобный письменный стол", uz: "Qulay ish stoli", en: "Work desk" },
        { ru: "Шкаф / гардероб и вешалка", uz: "Keng garderob va kiyim ilgichlar", en: "Wardrobe & clothes rack" },
        { ru: "Розетки рядом с кроватью", uz: "Krovat yonidagi qulay rozetkalar", en: "Sockets near bed" },
      ],
    },
    {
      titleRu: "Питание и напитки",
      titleUz: "Taomlar va ichimliklar",
      titleEn: "Food & Drinks",
      icon: "coffee",
      items: [
        { ru: "Потрясающий авторский завтрак (8,8)", uz: "Ajoyib mualliflik nonushtasi (8.8)", en: "Fabulous breakfast (Score 8.8)" },
        { ru: "Кофейня и бар на территории отеля", uz: "Mehmonxona hududidagi bar va qahvaxona", en: "On-site coffee house & bar" },
        { ru: "Доставка еды и напитков в номер", uz: "Xonaga taom va ichimlik yetkazish", en: "In-room dining & room service" },
        { ru: "Кофеварка / электрический чайник", uz: "Elektr choynak va kofe jihozlari", en: "Coffee / tea maker" },
        { ru: "Холодильник / мини-бар", uz: "Sovutgich / mini-bar", en: "Refrigerator / mini-bar" },
      ],
    },
    {
      titleRu: "Стойка регистрации и безопасность",
      titleUz: "Qabulxona va xavfsizlik",
      titleEn: "Front Desk & Safety",
      icon: "shield",
      items: [
        { ru: "Круглосуточная стойка регистрации 24/7", uz: "24/7 Qabulxona va ma'lumot stoli", en: "24-hour front desk" },
        { ru: "Ускоренная регистрация заезда и отъезда", uz: "Tezkor ro'yxatga olish va chiqarish", en: "Express check-in / check-out" },
        { ru: "Хранение багажа и сейфы", uz: "Yuk saqlash xonasi va seyflar", en: "Luggage storage & safe" },
        { ru: "Круглосуточная охрана и видеонаблюдение", uz: "Kechayu kunduz videokuzatuv va qo'riqlash", en: "24-hour security & CCTV" },
        { ru: "Вход по электронным смарт-картам", uz: "Elektron kirish kartalari", en: "Electronic keycard access" },
        { ru: "Датчики дыма и огнетушители", uz: "Yong'in datchiklari va xavfsizlik", en: "Smoke alarms & extinguishers" },
      ],
    },
    {
      titleRu: "Транспорт и общие услуги",
      titleUz: "Transport va umumiy xizmatlar",
      titleEn: "Transport & General Services",
      icon: "car",
      items: [
        { ru: "Бесплатная частная парковка на месте", uz: "Bepul xususiy avtoturargoh", en: "Free private parking on site" },
        { ru: "Трансфер от/до аэропорта", uz: "Aeroport transfer xizmati", en: "Airport shuttle service" },
        { ru: "Ежедневная уборка номеров", uz: "Kundalik tozalash xizmati", en: "Daily housekeeping" },
        { ru: "Номера для некурящих", uz: "Chekilmaydigan xonalar", en: "Non-smoking rooms" },
        { ru: "Семейные номера", uz: "Shinam oilaviy xonalar", en: "Spacious family rooms" },
        { ru: "Персонал говорит: узбекский, русский, английский", uz: "Xodimlar: o'zbek, rus, ingliz tillarida", en: "Staff speaks: Uzbek, Russian, English" },
      ],
    },
  ];

  return (
    <div className="flex flex-col bg-theme-main transition-colors duration-200">
      {/* 1. HERO HEADER */}
      <section
        aria-label="Services Header"
        className="relative bg-theme-secondary text-theme-main py-16 sm:py-24 border-b border-theme overflow-hidden transition-colors duration-200"
      >
        <GoldWavePattern variant="top-right" className="opacity-20 pointer-events-none" />

        <Container className="relative z-10 text-center">
          <RevealOnScroll variant="up">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-amber-400/15 text-amber-600 dark:text-amber-400 border border-amber-400/30 text-xs font-bold uppercase tracking-widest mb-4">
              ⭐ Booking.com: 8.8 — {language === 'ru' ? 'Потрясающе' : language === 'uz' ? 'Ajoyib' : 'Fabulous'}
            </div>
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-serif font-bold text-theme-main tracking-tight mb-4">
              {language === 'ru'
                ? 'Удобства и услуги — Coco Hotel'
                : language === 'uz'
                ? 'Qulayliklar va xizmatlar — Coco Hotel'
                : 'Amenities & Services — Coco Hotel'}
            </h1>
            <p className="text-base sm:text-lg text-theme-muted font-light max-w-3xl mx-auto leading-relaxed">
              {language === 'ru'
                ? 'Продуманные удобства для безупречного отдыха и деловых поездок в Ташкенте.'
                : language === 'uz'
                ? 'Toshkentda biznes va unutilmas hordiq uchun yaratilgan mukammal xizmatlar majmuasi.'
                : 'Thoughtfully curated amenities designed for business and serene relaxation in Tashkent.'}
            </p>
          </RevealOnScroll>
        </Container>
      </section>

      {/* 2. PRIMARY SERVICES CARDS */}
      <section aria-label="Services List" className="py-16 sm:py-20 bg-theme-main">
        <Container>
          {loading ? (
            <LoadingState />
          ) : error ? (
            <ErrorState onRetry={handleRetry} />
          ) : (
            <div className="space-y-20">
              <div>
                <RevealOnScroll variant="up">
                  <SectionTitle
                    subtitle={
                      language === 'ru'
                        ? 'Популярные услуги'
                        : language === 'uz'
                        ? 'Eng mashhur xizmatlar'
                        : 'Featured Hospitality'
                    }
                    title={
                      language === 'ru'
                        ? 'Главные удобства отеля'
                        : language === 'uz'
                        ? 'Asosiy mehmonxona qulayliklari'
                        : 'Core Hotel Services'
                    }
                  />
                </RevealOnScroll>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                  {services.map((service, idx) => (
                    <RevealOnScroll key={service.id} variant="up" delay={idx * 50}>
                      <div className="p-8 bg-theme-surface border border-theme rounded-2xl hover:border-amber-400 hover:shadow-xl transition-all duration-300 flex flex-col h-full group">
                        <div className="w-14 h-14 flex items-center justify-center rounded-2xl bg-amber-400/10 text-amber-500 mb-5 group-hover:scale-110 transition-transform duration-300">
                          <ServiceIcon name={service.icon || service.name} className="w-7 h-7" />
                        </div>
                        <h3 className="font-serif text-xl font-bold text-theme-main mb-2 group-hover:text-amber-500 transition-colors">
                          {service.name}
                        </h3>
                        <p className="text-sm text-theme-muted leading-relaxed font-light">
                          {service.description}
                        </p>
                      </div>
                    </RevealOnScroll>
                  ))}
                </div>
              </div>

              {/* 3. DETAILED CATEGORIZED AMENITIES (Booking.com style) */}
              <div>
                <RevealOnScroll variant="up">
                  <SectionTitle
                    subtitle={
                      language === 'ru'
                        ? 'Полный перечень удобств'
                        : language === 'uz'
                        ? "Barcha qulayliklar ro'yxati"
                        : 'Full Amenities Specification'
                    }
                    title={
                      language === 'ru'
                        ? 'Все удобства по категориям'
                        : language === 'uz'
                        ? "Kategoriyalar bo'yicha qulayliklar"
                        : 'Amenities by Category'
                    }
                  />
                </RevealOnScroll>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {amenityCategories.map((cat, idx) => {
                    const catTitle =
                      language === 'ru'
                        ? cat.titleRu
                        : language === 'uz'
                        ? cat.titleUz
                        : cat.titleEn;
                    return (
                      <div
                        key={idx}
                        className="bg-theme-surface border border-theme rounded-2xl p-7 shadow-xs hover:border-amber-400/50 transition-colors"
                      >
                        <div className="flex items-center gap-3 mb-5 pb-4 border-b border-theme">
                          <span className="w-10 h-10 rounded-xl bg-amber-400/10 text-amber-500 flex items-center justify-center font-bold">
                            ✓
                          </span>
                          <h3 className="font-serif text-lg font-bold text-theme-main">
                            {catTitle}
                          </h3>
                        </div>
                        <ul className="space-y-3">
                          {cat.items.map((item, itemIdx) => {
                            const itemText =
                              language === 'ru'
                                ? item.ru
                                : language === 'uz'
                                ? item.uz
                                : item.en;
                            return (
                              <li
                                key={itemIdx}
                                className="flex items-start gap-2.5 text-xs sm:text-sm text-theme-muted"
                              >
                                <span className="text-amber-500 font-bold shrink-0 mt-0.5">•</span>
                                <span>{itemText}</span>
                              </li>
                            );
                          })}
                        </ul>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* 4. Inquiry & Booking Callout */}
              <RevealOnScroll variant="up" delay={150}>
                <div className="p-8 sm:p-10 bg-theme-surface border border-theme rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl transition-colors duration-200">
                  <div className="max-w-xl space-y-2">
                    <h3 className="font-serif text-xl sm:text-2xl font-semibold text-theme-main">
                      {language === 'ru'
                        ? 'Нужен трансфер или индивидуальное обслуживание?'
                        : language === 'uz'
                        ? "Aeroportdan transfer yoki maxsus xizmat kerakmi?"
                        : 'Need airport transfer or personal concierge?'}
                    </h3>
                    <p className="text-sm text-theme-muted leading-relaxed font-light">
                      {language === 'ru'
                        ? 'Свяжитесь с нами круглосуточно по телефону +998 (88) 000-00-51 или забронируйте номер онлайн.'
                        : language === 'uz'
                        ? "Biz bilan 24/7 telefon orqali bog'laning: +998 (88) 000-00-51 yoki onlayn buyurtma bering."
                        : 'Contact our 24/7 concierge at +998 (88) 000-00-51 or submit a reservation inquiry online.'}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-4 shrink-0">
                    <Link
                      to="/booking"
                      className="inline-flex items-center justify-center px-7 py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-110 active:scale-[0.98] transition-all shadow-md"
                    >
                      {t('home.checkRooms')}
                    </Link>
                    <Link
                      to="/contact"
                      className="inline-flex items-center justify-center px-7 py-3.5 text-xs font-bold uppercase tracking-widest border border-theme-gold text-theme-gold hover:bg-theme-secondary rounded-full transition-colors"
                    >
                      {t('rooms.contactConcierge')}
                    </Link>
                  </div>
                </div>
              </RevealOnScroll>
            </div>
          )}
        </Container>
      </section>
    </div>
  );
}
