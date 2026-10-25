import type { Metadata } from "next";
import { Cairo, JetBrains_Mono, Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const cairo = Cairo({
  variable: "--font-cairo",
  subsets: ["arabic", "latin"],
  weight: ["300", "400", "500", "600", "700", "800", "900"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["400", "500", "700"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "مذكرة أوامر سيسكو الشاملة | Cisco IOS Commands Reference",
  description: "مرجع تفاعلي شامل لأوامر Cisco IOS - CCNA 200-301 و CCNP ENARSI مع بحث فوري وفلترة",
  keywords: ["Cisco", "IOS", "CCNA", "CCNP", "OSPF", "EIGRP", "BGP", "VLAN", "ACL", "NAT", "Cisco Commands"],
  authors: [{ name: "Z.ai Network Engineering" }],
  icons: {
    icon: "https://z-cdn.chatglm.cn/z-ai/static/logo.svg",
  },
  openGraph: {
    title: "مذكرة أوامر سيسكو الشاملة",
    description: "مرجع تفاعلي لأوامر Cisco IOS - CCNA & CCNP",
    siteName: "Cisco IOS Reference",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl" suppressHydrationWarning>
      <body
        className={`${cairo.variable} ${jetbrainsMono.variable} ${inter.variable} antialiased bg-background text-foreground font-sans`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
