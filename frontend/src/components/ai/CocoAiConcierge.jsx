import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../../hooks/useLanguage';
import { sendChatMessage } from '../../api/ai';

// Helper to format AI markdown into styled React elements
function FormattedMessage({ content, onNavigate }) {
  if (!content) return null;

  // Split lines
  const lines = content.split('\n');

  return (
    <div className="space-y-1.5 text-sm leading-relaxed">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (!trimmed) {
          return <div key={idx} className="h-1" />;
        }

        // Horizontal rules
        if (trimmed === '---') {
          return <hr key={idx} className="my-2 border-stone-200 dark:border-stone-700/60" />;
        }

        // Subheaders
        if (trimmed.startsWith('### ') || trimmed.startsWith('## ')) {
          const headerText = trimmed.replace(/^#+\s*/, '');
          return (
            <h4 key={idx} className="font-bold text-amber-600 dark:text-amber-400 mt-2 mb-1 text-sm flex items-center gap-1.5">
              {headerText}
            </h4>
          );
        }

        // Bullet point
        const isBullet = trimmed.startsWith('* ') || trimmed.startsWith('- ') || trimmed.startsWith('• ');
        const cleanLine = isBullet ? trimmed.replace(/^[\*\-•]\s*/, '') : trimmed;

        // Parse markdown bold and links
        const parts = [];
        // Regex matches [title](url) OR **bold**
        const tokenRegex = /(\[.*?\]\(.*?\)|\*\*.*?\*\*)/g;
        let lastIndex = 0;
        let match;

        while ((match = tokenRegex.exec(cleanLine)) !== null) {
          if (match.index > lastIndex) {
            parts.push(cleanLine.substring(lastIndex, match.index));
          }

          const token = match[0];
          if (token.startsWith('[') && token.includes('](')) {
            const linkMatch = token.match(/\[(.*?)\]\((.*?)\)/);
            if (linkMatch) {
              const [, title, url] = linkMatch;
              const isInternal = url.startsWith('/');
              parts.push(
                <button
                  key={`${idx}-${match.index}`}
                  type="button"
                  onClick={() => {
                    if (isInternal) {
                      onNavigate(url);
                    } else {
                      window.open(url, '_blank', 'noopener,noreferrer');
                    }
                  }}
                  className="inline-flex items-center gap-1 text-amber-600 dark:text-amber-400 underline font-semibold hover:text-amber-500 transition-colors mx-1 cursor-pointer"
                >
                  {title} ↗
                </button>
              );
            }
          } else if (token.startsWith('**') && token.endsWith('**')) {
            parts.push(
              <strong key={`${idx}-${match.index}`} className="font-bold text-stone-950 dark:text-white">
                {token.slice(2, -2)}
              </strong>
            );
          }
          lastIndex = match.index + token.length;
        }

        if (lastIndex < cleanLine.length) {
          parts.push(cleanLine.substring(lastIndex));
        }

        return (
          <p key={idx} className={isBullet ? 'flex items-start gap-1.5 pl-1 text-[13.5px]' : 'text-[13.5px]'}>
            {isBullet && <span className="text-amber-500 font-bold shrink-0">•</span>}
            <span>{parts}</span>
          </p>
        );
      })}
    </div>
  );
}

export default function CocoAiConcierge() {
  const { language } = useLanguage();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef(null);


  // Initial welcome message localized
  const getInitialMessage = () => {
    if (language === 'ru') {
      return 'Здравствуйте! Я ваш персональный консьерж Coco Hotel. С удовольствием подскажу цены на номера, время завтрака, трансфер или порекомендую интересные места в Ташкенте!';
    }
    if (language === 'uz') {
      return 'Assalomu alaykum! Men Coco Hotel rasmiy virtual konsyerjiman. Sizga xonalar narxlari, nonushta, aeroport transferi yoki Toshkent bo‘ylab sayohat bo‘yicha bajonidil yordam beraman!';
    }
    return 'Welcome to Coco Hotel! I am your personal AI concierge. How can I assist you with room reservations, breakfast, airport transfers, or visiting Tashkent?';
  };

  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: getInitialMessage(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  // Update initial message when language changes if no interaction yet
  useEffect(() => {
    if (messages.length === 1 && messages[0].sender === 'ai') {
      setMessages([
        {
          sender: 'ai',
          text: getInitialMessage(),
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    }
  }, [language]);

  // Auto-scroll to latest message
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, loading]);

  const quickQuestions = language === 'ru' ? [
    '🥐 Во сколько завтрак?',
    '💰 Цены на номера',
    '🚕 Трансфер из аэропорта',
    '🗺️ Куда сходить в Ташкенте?',
  ] : language === 'uz' ? [
    '🥐 Nonushta qachon?',
    '💰 Xonalar narxlari',
    '🚕 Aeroport transferi',
    '🗺️ Toshkentda qayerga borish kerak?',
  ] : [
    '🥐 Breakfast hours',
    '💰 Room rates',
    '🚕 Airport transfer',
    '🗺️ Places to visit in Tashkent',
  ];

  const handleSend = async (textToSend) => {
    const text = (textToSend || inputMessage).trim();
    if (!text || loading) return;

    const userMsg = {
      sender: 'user',
      text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInputMessage('');
    setLoading(true);

    try {
      // Send chat history for context
      const historyPayload = newMessages.map((m) => ({
        sender: m.sender,
        text: m.text,
      }));

      const res = await sendChatMessage(text, historyPayload);
      const replyText = res?.reply || (
        language === 'ru'
          ? 'Пожалуйста, обратитесь на нашу круглосуточную стойку регистрации: +998 88 000-00-51.'
          : 'Iltimos, 24/7 qabulxonamizga murojaat qiling: +998 88 000-00-51.'
      );

      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: replyText,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: language === 'ru'
            ? 'Произошла ошибка связи. Пожалуйста, позвоните нам: +998 88 000-00-51.'
            : 'Bog‘lanishda xatolik yuz berdi. Iltimos, bizga qo‘ng‘iroq qiling: +998 88 000-00-51.',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Speech Recognition (Voice input)
  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert(language === 'ru' ? 'Ваш браузер не поддерживает голосовой ввод.' : 'Brauzeringiz ovozli kiritishni qo‘llab-quvvatlamaydi.');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === 'ru' ? 'ru-RU' : language === 'uz' ? 'uz-UZ' : 'en-US';
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (transcript) {
        handleSend(transcript);
      }
    };

    recognition.start();
  };

  return (
    <>
      {/* 1. Floating AI Concierge Button */}
      <div className="fixed bottom-5 right-5 sm:bottom-7 sm:right-7 z-50">
        {!isOpen && (
          <button
            type="button"
            onClick={() => setIsOpen(true)}
            aria-label="Coco AI Concierge Chat"
            className="group relative flex items-center gap-3 px-4 sm:px-5 py-3.5 rounded-full bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600 text-stone-950 font-bold shadow-2xl shadow-amber-500/30 hover:scale-105 active:scale-95 transition-all cursor-pointer border border-amber-300"
          >
            {/* Pulsing indicator */}
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-stone-950 opacity-60" />
              <span className="relative inline-flex rounded-full h-3 w-3 bg-stone-950" />
            </span>

            <span className="text-xl shrink-0">✨</span>
            <div className="flex flex-col text-left">
              <span className="text-xs uppercase tracking-wider font-extrabold leading-none">
                Coco AI
              </span>
              <span className="text-[10px] opacity-90 font-medium leading-tight">
                24/7 Concierge
              </span>
            </div>
          </button>
        )}
      </div>

      {/* 2. Interactive AI Concierge Chat Modal */}
      {isOpen && (
        <div className="fixed inset-0 sm:inset-auto sm:bottom-6 sm:right-6 sm:w-[420px] sm:h-[620px] z-50 flex flex-col bg-white dark:bg-[#12161f] border border-stone-200 dark:border-stone-800 rounded-none sm:rounded-3xl shadow-2xl overflow-hidden transition-all duration-300 animate-fadeIn">
          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 bg-gradient-to-r from-stone-900 via-stone-900 to-stone-950 text-white border-b border-amber-500/30">
            <div className="flex items-center gap-3">
              <div className="relative w-10 h-10 rounded-full bg-amber-500/20 border border-amber-400 flex items-center justify-center text-xl text-amber-400 shadow-md">
                ✨
                <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 border-2 border-stone-900" />
              </div>
              <div>
                <h3 className="font-serif font-bold text-base text-amber-300 flex items-center gap-1.5">
                  Coco AI Concierge
                </h3>
                <p className="text-[11px] text-stone-400 font-light">
                  {language === 'ru' ? 'Онлайн • Помощник отеля' : language === 'uz' ? 'Onlayn • Mehmonxona yordamchisi' : 'Online • Hotel Assistant'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              {/* Close Button */}
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="w-8 h-8 rounded-full flex items-center justify-center text-stone-400 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
                aria-label="Close Chat"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 bg-stone-50/60 dark:bg-[#0c0e14]">
            {messages.map((msg, index) => {
              const isUser = msg.sender === 'user';
              return (
                <div
                  key={index}
                  className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                      isUser
                        ? 'bg-amber-500 text-stone-950 font-medium rounded-br-xs shadow-md'
                        : 'bg-white dark:bg-[#1a202c] text-stone-800 dark:text-stone-100 border border-stone-200 dark:border-stone-800 rounded-bl-xs shadow-sm'
                    }`}
                  >
                    {isUser ? (
                      <p className="whitespace-pre-line">{msg.text}</p>
                    ) : (
                      <FormattedMessage
                        content={msg.text}
                        onNavigate={(url) => {
                          navigate(url);
                          if (window.innerWidth < 640) setIsOpen(false);
                        }}
                      />
                    )}
                  </div>
                  <span className="text-[10px] text-stone-400 mt-1 px-1">
                    {msg.time}
                  </span>
                </div>
              );
            })}

            {/* Loading indicator */}
            {loading && (
              <div className="flex items-start gap-2">
                <div className="bg-white dark:bg-[#1a202c] border border-stone-200 dark:border-stone-800 rounded-2xl rounded-bl-xs px-4 py-3 shadow-sm">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce" />
                    <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce [animation-delay:0.2s]" />
                    <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce [animation-delay:0.4s]" />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Suggestions Chips */}
          <div className="px-4 py-2 bg-white dark:bg-[#12161f] border-t border-stone-200 dark:border-stone-800 overflow-x-auto no-scrollbar flex items-center gap-2">
            {quickQuestions.map((q, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSend(q.replace(/^[^\w\sа-яА-ЯёЁo'g'shch]+/u, '').trim())}
                className="whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-semibold bg-stone-100 dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:bg-amber-500/15 hover:text-amber-600 dark:hover:text-amber-400 border border-stone-200 dark:border-stone-700 transition-colors cursor-pointer shrink-0"
              >
                {q}
              </button>
            ))}
          </div>

          {/* Input & Voice Controls */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="p-3 bg-white dark:bg-[#12161f] border-t border-stone-200 dark:border-stone-800 flex items-center gap-2"
          >
            {/* Voice Input Button */}
            <button
              type="button"
              onClick={handleVoiceInput}
              title={language === 'ru' ? 'Голосовой ввод' : 'Ovozli kiritish'}
              className={`p-2.5 rounded-full border transition-all cursor-pointer ${
                isListening
                  ? 'bg-rose-500 text-white animate-pulse border-rose-600'
                  : 'bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-300 hover:text-amber-500 border-stone-200 dark:border-stone-700'
              }`}
            >
              🎤
            </button>

            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={
                language === 'ru'
                  ? 'Задайте вопрос консьержу...'
                  : language === 'uz'
                  ? 'Konsyerjga savol bering...'
                  : 'Ask Coco Concierge...'
              }
              className="flex-1 px-4 py-2.5 bg-stone-100 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700 rounded-xl text-sm text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:border-amber-500 transition-colors"
            />

            <button
              type="submit"
              disabled={!inputMessage.trim() || loading}
              className="p-2.5 rounded-xl bg-amber-500 text-stone-950 hover:bg-amber-400 disabled:opacity-40 disabled:cursor-not-allowed transition-colors font-bold cursor-pointer shadow-md"
            >
              <svg className="w-5 h-5 rotate-90" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
