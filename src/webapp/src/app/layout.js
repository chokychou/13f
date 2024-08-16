import { Inter } from "next/font/google";
import "./globals.css";
import Footer from "./components/Footer"

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "13 web app",
  description: "A 13 web app wip",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
