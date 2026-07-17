import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Zydrakon AI | Space-Age AI Chatbot",
  description: "Zydrakon AI is a high-performance, cost-free AI chatbot leveraging OpenRouter free-tier LLMs, SQLite query caching, and sqlite-backed rate limiting.",
  authors: [{ name: "Zydrakon AI Team" }],
  keywords: ["Zydrakon", "AI Chatbot", "FastAPI Chatbot", "OpenRouter Chatbot", "Next.js AI Chatbot"],
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased text-gray-200 bg-[#030712]`} suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
