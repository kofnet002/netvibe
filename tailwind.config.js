/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./netvibe/**/*.{html,js}", ],
  theme: {
    extend: {
      colors: { // your theme colours, etc.
      },
    },
  },
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}