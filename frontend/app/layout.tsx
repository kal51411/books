import './globals.css';

export const metadata = {
  title: 'NyayaGPT',
  description: 'AI-Powered Indian Legal Research and Assistance Platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
