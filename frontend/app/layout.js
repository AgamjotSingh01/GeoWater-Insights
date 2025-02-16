import "./globals.css";
import Navbar1 from "@/Components/Navbar";
import 'bootstrap/dist/css/bootstrap.min.css';

export const metadata = {
  title: "Geo Water",
  description: "HMMMMMM",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar1 />
        {children}
      </body>
    </html>
  );
}
