import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "bg-dark": "#0f172a",
        "bg-darker": "#020617",
        "panel-bg": "rgba(30, 41, 59, 0.7)",
        "panel-border": "rgba(255, 255, 255, 0.1)",
        "text-main": "#f8fafc",
        "text-muted": "#94a3b8",
        accent: "#38bdf8",
        "accent-hover": "#0284c7",
        error: "#ef4444",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      animation: {
        shimmer: "shimmer 1.5s infinite",
        spin: "spin 1s linear infinite",
      },
      keyframes: {
        shimmer: {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
        spin: {
          to: { transform: "rotate(360deg)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
