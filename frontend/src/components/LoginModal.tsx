"use client";

import React, { useState } from "react";
import { ShieldAlert, Sparkles, LogIn } from "lucide-react";

interface LoginModalProps {
  onSuccess: (token: string) => void;
}

export function LoginModal({ onSuccess }: LoginModalProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // Form fields
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      const endpoint = isLogin ? "/api/auth/login" : "/api/auth/register";
      const payload = isLogin 
        ? { email, password } 
        : { email, password, name };
        
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || "Authentication failed");
      }
      
      localStorage.setItem("zydrakon_token", data.access_token);
      onSuccess(data.access_token);
    } catch (err: any) {
      setError(err.message || "Failed to authenticate");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-4">
      <div className="bg-[var(--bg-main)] p-8 rounded-2xl border border-[var(--border-color)] shadow-xl w-full max-w-md flex flex-col items-center relative overflow-hidden">
        
        <div className="p-4 bg-[#f3f1eb] dark:bg-[#22221f] border border-[var(--border-color)] rounded-full mb-6">
          <Sparkles className="w-8 h-8 text-[var(--accent-color)]" />
        </div>
        
        <h2 className="text-2xl font-bold mb-2">
          {isLogin ? "Welcome Back" : "Create Account"}
        </h2>
        
        <p className="text-[var(--text-secondary)] text-sm mb-6 text-center">
          {isLogin 
            ? "Log in to continue and access your personalized chat sessions." 
            : "Sign up to start chatting with Zydrakon AI."}
        </p>

        {error && (
          <div className="flex items-center gap-2 p-3 bg-red-950/20 border border-red-900/30 text-red-400 rounded-xl text-xs mb-6 w-full shadow-sm">
            <ShieldAlert className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="w-full space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-xs font-semibold text-[var(--text-secondary)] mb-1 uppercase tracking-wide">
                Name
              </label>
              <input 
                type="text" 
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="John Doe"
                className="w-full bg-[var(--bg-input)] border border-[var(--border-color)] rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[var(--accent-color)] focus:ring-1 focus:ring-[var(--accent-color)] transition-all text-[var(--text-main)] placeholder:text-slate-500"
                required={!isLogin}
              />
            </div>
          )}
          
          <div>
            <label className="block text-xs font-semibold text-[var(--text-secondary)] mb-1 uppercase tracking-wide">
              Email
            </label>
            <input 
              type="email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full bg-[var(--bg-input)] border border-[var(--border-color)] rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[var(--accent-color)] focus:ring-1 focus:ring-[var(--accent-color)] transition-all text-[var(--text-main)] placeholder:text-slate-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-xs font-semibold text-[var(--text-secondary)] mb-1 uppercase tracking-wide">
              Password
            </label>
            <input 
              type="password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-[var(--bg-input)] border border-[var(--border-color)] rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[var(--accent-color)] focus:ring-1 focus:ring-[var(--accent-color)] transition-all text-[var(--text-main)] placeholder:text-slate-500"
              required
              minLength={6}
            />
          </div>
          
          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full mt-4 bg-[var(--accent-color)] hover:bg-[var(--accent-hover)] text-white font-semibold rounded-xl px-4 py-2.5 transition-colors flex items-center justify-center gap-2 shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <span className="animate-pulse">Processing...</span>
            ) : (
              <>
                <LogIn className="w-4 h-4" />
                {isLogin ? "Sign In" : "Sign Up"}
              </>
            )}
          </button>
        </form>

        <div className="mt-6 text-sm text-[var(--text-secondary)]">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button 
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            className="text-[var(--accent-color)] font-semibold hover:underline"
          >
            {isLogin ? "Sign up" : "Log in"}
          </button>
        </div>
      </div>
    </div>
  );
}
