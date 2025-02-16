import React from "react";

export default function Card({ title, content }) {
    return (
        <div className="card text-center col-3 blurCard">
            <div className="card-body">
                <h5 className="card-title text-white">{title}</h5>
                <p className="card-text lead text-light">{content}</p>
            </div>
        </div>
    )
}