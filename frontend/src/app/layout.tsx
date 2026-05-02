import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: '--font-inter' });
const outfit = Outfit({ subsets: ["latin"], variable: '--font-outfit' });

export const metadata: Metadata = {
  title: "Gourmet AI | Premium Restaurant Recommendations",
  description: "Discover curated dining experiences powered by intelligent AI ranking.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${outfit.variable}`}>
      <body className="font-sans antialiased text-slate-200">
        <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden bg-[#020617]">
          <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-violet-600/20 blur-[120px] rounded-full opacity-50" />
          <div className="absolute bottom-[10%] right-[10%] w-[40%] h-[40%] bg-fuchsia-600/10 blur-[100px] rounded-full opacity-30" />
          <div className="absolute top-[20%] right-[20%] w-[30%] h-[30%] bg-blue-600/10 blur-[100px] rounded-full opacity-20" />
        </div>
        {children}
      </body>
    </html>
  );
}
