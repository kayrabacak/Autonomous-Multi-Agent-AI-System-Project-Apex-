import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
    startOnLoad: false,
    theme: 'dark',
    securityLevel: 'loose',
    fontFamily: 'Inter, sans-serif',
});

const Mermaid = ({ chart }) => {
    const containerRef = useRef(null);

    useEffect(() => {
        if (containerRef.current && chart) {
            mermaid.render(`mermaid-${Date.now()}`, chart).then(({ svg }) => {
                containerRef.current.innerHTML = svg;
            });
        }
    }, [chart]);

    return <div className="mermaid-chart" ref={containerRef} style={{ textAlign: 'center', margin: '2rem 0' }} />;
};

export default Mermaid;
