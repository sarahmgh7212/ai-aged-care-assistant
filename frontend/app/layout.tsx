import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Aged Care Information Assistant',
  description: 'AI-powered aged care information assistant',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
