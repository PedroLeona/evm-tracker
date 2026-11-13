import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": BACKEND_URL,
    },
  },
});
