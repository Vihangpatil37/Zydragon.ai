"use client";

import React from "react";

interface AgentLoaderProps {
  isDarkMode?: boolean;
  color?: string;
  size?: number;
}

// ═══════════════════════════════════════════════════════
// Liquid Iridescent Chromatic Orb Video Loader Component
// Formatted with a clean circular frame & agent-colored border glow
// ═══════════════════════════════════════════════════════

export function AgentLoader({ isDarkMode = true, color = "#e26e4a", size = 52 }: AgentLoaderProps) {
  if (!isDarkMode) {
    return (
      <div 
        className="w-10 h-10 rounded-full border-2 border-transparent border-t-[var(--accent-color)] border-r-[var(--accent-color)] animate-spin opacity-80" 
      />
    );
  }

  return (
    <div 
      className="relative flex items-center justify-center rounded-full overflow-hidden select-none shrink-0 border shadow-lg backdrop-blur-md"
      style={{ 
        width: size, 
        height: size,
        borderColor: `${color}45`,
        backgroundColor: "#000000",
        boxShadow: `0 0 20px ${color}25, 0 4px 16px rgba(0,0,0,0.5)`
      }}
    >
      <video
        src="/loader.mp4"
        autoPlay
        loop
        muted
        playsInline
        className="w-full h-full object-cover rounded-full pointer-events-none scale-110"
      />
    </div>
  );
}
