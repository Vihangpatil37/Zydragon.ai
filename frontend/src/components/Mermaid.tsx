"use client";

import React, { useEffect, useRef, useState } from "react";
import mermaid from "mermaid";

interface MermaidProps {
  chart: string;
  isDarkMode: boolean;
}

export default function Mermaid({ chart, isDarkMode }: MermaidProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [svg, setSvg] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 1. Configure and Initialize Mermaid
    try {
      mermaid.initialize({
        startOnLoad: false,
        theme: isDarkMode ? "dark" : "default",
        securityLevel: "loose",
        suppressErrorRendering: true,
        fontFamily: "var(--font-inter), sans-serif",
        themeVariables: {
          background: isDarkMode ? "#1b1b18" : "#fbfaf7",
          primaryColor: isDarkMode ? "#e26e4a" : "#cc5a37",
          lineColor: isDarkMode ? "#32322e" : "#e6e4de",
          primaryTextColor: isDarkMode ? "#e6e6e2" : "#191919",
          secondaryColor: isDarkMode ? "#22221f" : "#f7f5f0",
          tertiaryColor: isDarkMode ? "#292926" : "#ffffff",
          // Subgraphs / Clusters customization to prevent white background
          clusterBkg: isDarkMode ? "#22221f" : "#f7f5f0",
          clusterBorder: isDarkMode ? "#32322e" : "#e6e4de",
          subgraphBkg: isDarkMode ? "#22221f" : "#f7f5f0",
          subgraphBorderColor: isDarkMode ? "#32322e" : "#e6e4de",
          subgraphTitleColor: isDarkMode ? "#e6e6e2" : "#191919",
          // Nodes customization
          nodeBkg: isDarkMode ? "#22221f" : "#ffffff",
          nodeBorder: isDarkMode ? "#32322e" : "#e6e4de",
          textColor: isDarkMode ? "#e6e6e2" : "#191919",
          mainBkg: isDarkMode ? "#1b1b18" : "#fbfaf7",
        }
      });
      // Override parseError to prevent global uncaught exceptions during streaming
      // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
      (mermaid as any).parseError = (err: any, _hash: any) => {
        console.warn("Mermaid silent parse warning:", err);
      };
    } catch (e) {
      console.error("Failed to initialize mermaid", e);
    }

    let isMounted = true;

    // Helper to sanitize light style definitions in dark mode
    const adjustColorsForDarkMode = (chartText: string): string => {
      let adjusted = chartText;
      
      // Replace fill:#HEX colors with dark versions if they are too light
      adjusted = adjusted.replace(/fill:#([A-Fa-f0-9]{3,6})/gi, (match, hex) => {
        let fullHex = hex;
        if (hex.length === 3) {
          fullHex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
        }
        
        const r = parseInt(fullHex.substring(0, 2), 16);
        const g = parseInt(fullHex.substring(2, 4), 16);
        const b = parseInt(fullHex.substring(4, 6), 16);
        
        // Luminance check (approximate)
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        
        if (luminance > 0.4) {
          // Scale down brightness to ~15% for a rich dark shade
          const dr = Math.round(r * 0.15);
          const dg = Math.round(g * 0.15);
          const db = Math.round(b * 0.15);
          
          const hexR = Math.max(22, dr).toString(16).padStart(2, '0');
          const hexG = Math.max(22, dg).toString(16).padStart(2, '0');
          const hexB = Math.max(22, db).toString(16).padStart(2, '0');
          return `fill:#${hexR}${hexG}${hexB}`;
        }
        return match;
      });

      // Replace named light colors
      const lightColorMap: Record<string, string> = {
        'white': '#1b1b18',
        '#ffffff': '#1b1b18',
        '#fff': '#1b1b18',
        'lightgray': '#22221f',
        'lightgrey': '#22221f',
        'gray': '#252522',
        'grey': '#252522',
        'pink': '#35181d',
        'lightblue': '#182435',
        'lightgreen': '#18351c',
        'yellow': '#353018',
      };
      
      for (const [lightColor, darkColor] of Object.entries(lightColorMap)) {
        const regex = new RegExp(`fill:\\s*${lightColor}\\b`, 'gi');
        adjusted = adjusted.replace(regex, `fill:${darkColor}`);
      }

      // Ensure text colors inside styling are light
      adjusted = adjusted.replace(/color:#([A-Fa-f0-9]{3,6})/gi, 'color:#e6e6e2');
      adjusted = adjusted.replace(/color:\s*(black|darkgrey|darkgray|#000000|#000)\b/gi, 'color:#e6e6e2');

      return adjusted;
    };

    const renderChart = async () => {
      if (!ref.current) return;
      try {
        setError(null);
        // Generate a random valid id
        const id = `mermaid-svg-${Math.random().toString(36).substring(2, 11)}`;
        
        // Clean up common LLM syntax issues (e.g. unquoted link labels with parentheses)
        let sanitizedChart = chart;
        sanitizedChart = sanitizedChart.replace(/\|([^"|\r\n]+)\|/g, '|"$1"|');
        
        // Apply dark mode adjustments if active
        if (isDarkMode) {
          sanitizedChart = adjustColorsForDarkMode(sanitizedChart);
        }
        
        // Render the diagram
        const { svg: renderedSvg } = await mermaid.render(id, sanitizedChart);
        
        if (isMounted) {
          setSvg(renderedSvg);
        }
      } catch (err: unknown) {
        console.error("Mermaid render error:", err);
        if (isMounted) {
          setError(err instanceof Error ? err.message : "Invalid Mermaid syntax");
        }
      }
    };

    renderChart();

    return () => {
      isMounted = false;
    };
  }, [chart, isDarkMode]);

  if (error) {
    return (
      <div className="my-4 p-4 rounded-xl border border-red-500/20 bg-red-500/10 text-red-400 dark:text-red-300 font-mono text-xs max-w-full overflow-x-auto shadow-inner select-text">
        <div className="font-bold flex items-center gap-1.5 mb-1.5 text-red-500">
          ⚠️ Diagram Rendering Failed
        </div>
        <p className="opacity-90 leading-relaxed">{error}</p>
        <details className="mt-2 opacity-60 cursor-pointer select-none">
          <summary className="text-[10px] hover:underline font-sans">Show original source</summary>
          <pre className="mt-2 p-2 bg-black/20 rounded font-mono text-[10px] whitespace-pre select-text text-slate-300">{chart}</pre>
        </details>
      </div>
    );
  }

  return (
    <div 
      ref={ref} 
      className="my-4 p-2 overflow-x-auto scrollbar-thin select-none max-w-full"
    >
      {svg ? (
        <div 
          className="select-none [&>svg]:mx-auto [&>svg]:block [&>svg]:max-w-full [&>svg]:h-auto"
          dangerouslySetInnerHTML={{ __html: svg }}
        />
      ) : (
        <div className="text-xs text-[var(--text-secondary)] animate-pulse font-mono py-4 text-center">
          Compiling vector diagram...
        </div>
      )}
    </div>
  );
}
