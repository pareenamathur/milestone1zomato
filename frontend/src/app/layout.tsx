import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Restaurant Recommender",
  description: "Experience premium AI-powered restaurant recommendations with style.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
          <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-violet-600/10 blur-[120px] rounded-full animate-pulse" />
          <div className="absolute bottom-[10%] right-[10%] w-[30%] h-[30%] bg-indigo-600/10 blur-[100px] rounded-full animate-pulse delay-700" />
        </div>
        {children}
      </body>
    </html>
  );
}
