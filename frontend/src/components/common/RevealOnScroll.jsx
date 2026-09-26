import { useEffect, useRef, useState } from 'react';

/**
 * Reusable RevealOnScroll component using IntersectionObserver.
 * Supports: 'up', 'fade', 'left', 'right' directions, configurable delay & duration.
 * Respects prefers-reduced-motion: reduce and falls back safely if IntersectionObserver is unavailable.
 */
export default function RevealOnScroll({
  children,
  variant = 'up',
  delay = 0,
  duration = 600,
  threshold = 0.15,
  className = '',
  as: Component = 'div',
  ...props
}) {
  const [isVisible, setIsVisible] = useState(() => {
    if (typeof window === 'undefined') return true;
    if (typeof IntersectionObserver === 'undefined') return true;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return true;
    return false;
  });
  const elementRef = useRef(null);

  useEffect(() => {
    if (isVisible) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    const el = elementRef.current;
    if (el) {
      observer.observe(el);
    }

    return () => {
      if (el) {
        observer.unobserve(el);
      }
    };
  }, [isVisible, threshold]);

  // Variant transformations when hidden
  const getHiddenTransform = () => {
    switch (variant) {
      case 'up':
        return 'translate-y-8';
      case 'left':
        return '-translate-x-8';
      case 'right':
        return 'translate-x-8';
      case 'fade':
      default:
        return 'translate-y-0';
    }
  };

  const style = {
    transitionDuration: `${duration}ms`,
    transitionDelay: `${delay}ms`,
  };

  return (
    <Component
      ref={elementRef}
      style={style}
      className={`transition-all ease-out ${
        isVisible ? 'opacity-100 translate-x-0 translate-y-0' : `opacity-0 ${getHiddenTransform()}`
      } ${className}`}
      {...props}
    >
      {children}
    </Component>
  );
}
