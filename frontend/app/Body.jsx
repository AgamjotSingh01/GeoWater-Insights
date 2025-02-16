'use client'
import React from "react";
import Card from "@/Components/Card";
import Link from "next/link";

import './Body.css';


export default function Body() {
    return (
        <div>
            <div className="container py-5">
                <div className="display-1 text-center">GeoWater Insights </div>
                <div className="h2 text-muted text-center">Harness advanced analytics for effective groundwater management.</div>
            </div>

            <div className="container-fluid d-flex justify-content-around py-5">
                <Card
                    title={'Revolutionizing Groundwater Management'}
                    content={'Our innovative solution for the Ministry of Jal Shakti combines advanced modeling and geolocation mapping to deliver accurate groundwater level predictions. With a user-friendly interface tailored to your location, rainfall, and aquifer type, make informed decisions for sustainable water resource management.'}
                />
                <Card
                    title={'Key Features'}
                    content={'Our solution uses machine learning for accurate groundwater forecasts and precise geolocation mapping for visualizing levels. With a user-friendly interface and integrated data, it offers tailored insights and holistic monitoring. Designed for scalability and security, it adapts to user needs while protecting data.'}
                />
                <Card
                    title={'Use Cases'}
                    content={'Our solution enables water resource management by monitoring and managing groundwater sustainably. It supports agricultural planning by enhancing irrigation and crop decisions and aids urban development through sustainable construction practices. Additionally, it facilitates research and education by providing valuable insights into groundwater trends.'}
                />
            </div>

            <div className="container-fluid d-flex justify-content-center py-5">
                <Link href={'/Feature'}>
                    <button className="pushable">
                        <span className="shawdow"></span>
                        <span className="edge"></span>
                        <span className="front">Get started</span>
                    </button>
                </Link>
            </div>
        </div>
    )
}