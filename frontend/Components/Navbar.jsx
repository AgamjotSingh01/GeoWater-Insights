'use client'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Image from 'next/image';
import Link from 'next/link';

function Navbar1() {
  return (
    <div className='d-flex justify-content-between container-fluid align-items-center blurNav pb-3 sticky-top'>
        <div className='navbar-brand'>
            <Link href={'/'}>
                <Image
                    src='/Logo.png'
                    alt='Logo'
                    width={110}
                    height={95}
                />
            </Link>
        </div>
        <div className='d-flex justify-content-start align-items-center'>
            <div className='pe-3'>
                <div className=''>
                    <Link href={'/'} className='p-2 h4 text-decoration-none'>Home</Link>
                    <Link href={'/Feature'} className='p-2 h4 text-decoration-none'>Features</Link>
                    <Link href={'/'} className='p-2 h4 text-decoration-none'>About us</Link>
                    <Link href={'/'} className='p-2 h4 text-decoration-none'>Contact</Link>
                </div>
            </div>
        </div>

    </div>
  );
}

export default Navbar1;