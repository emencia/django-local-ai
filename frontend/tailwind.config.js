const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx,vue}',
    './node_modules/@snowind/**/*.{vue,js,ts}',
  ],
  darkMode: 'class',
  plugins: [
    require('@tailwindcss/forms'),
    require('@snowind/plugin'),
    require('tailwindcss-semantic-colors')
  ],
  theme: {
    screens: {
      'xs': '500px',
      'xxs': '430px',
      ...defaultTheme.screens,
    },
  }
}