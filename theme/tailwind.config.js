/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py',
  ],
  darkMode: false,
  theme: {
    extend: {
      colors: {
        blush: '#FFDFB3',  // Tu color personalizado
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
