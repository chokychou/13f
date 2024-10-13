import { Inter } from "next/font/google";
import { ThemeProvider } from '../components/providers/theme-provider'
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "13 web app",
  description: "A 13 web app wip",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
        >
          <main>{children}</main>
        </ThemeProvider>
      </body>
    </html>
  );
}
