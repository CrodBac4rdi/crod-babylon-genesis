/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'crod-primary': '#FF6B6B',
        'crod-secondary': '#4ECDC4',
        'crod-dark': '#1A1A2E',
        'crod-darker': '#0F0F1E',
        'crod-accent': '#FFD93D',
        'crod-quantum': '#9B5DE5',
      },
      animation: {
        'pulse-quantum': 'pulseQuantum 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'rotate-slow': 'rotate 20s linear infinite',
      },
      keyframes: {
        pulseQuantum: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.3 },
        },
        rotate: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}