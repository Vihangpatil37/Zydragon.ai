"use client";

import React from "react";

interface AgentLoaderProps {
  agentId?: string;
  color?: string;
  size?: number;
}

// ═══════════════════════════════════════════════════════
// Liquid Iridescent Orb Video Loader Component
// Renders the futuristic 3D liquid chromatic orb video
// ═══════════════════════════════════════════════════════

export function AgentLoader({ size = 56 }: AgentLoaderProps) {
  return (
    <div 
      className="relative flex items-center justify-center rounded-full overflow-hidden select-none shrink-0"
      style={{ width: size, height: size }}
    >
      <video
        src="/loader.mp4"
        autoPlay
        loop
        muted
        playsInline
        className="w-full h-full object-cover rounded-full mix-blend-screen scale-110 pointer-events-none"
      />
    </div>
  );
}
