import { BrowserRouter } from 'react-router-dom';
import AppRouter from './router/AppRouter';
import { ThemeProvider } from './context/ThemeProvider';
import { LanguageProvider } from './context/LanguageProvider';
import CocoAiConcierge from './components/ai/CocoAiConcierge';

export default function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <BrowserRouter>
          <AppRouter />
          <CocoAiConcierge />
        </BrowserRouter>
      </LanguageProvider>
    </ThemeProvider>
  );
}
