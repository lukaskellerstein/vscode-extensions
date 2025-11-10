import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
// @ts-ignore
import styles from './App.css';

// Inject CSS into the document
const style = document.createElement('style');
style.textContent = styles;
document.head.appendChild(style);

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<App />);
}
