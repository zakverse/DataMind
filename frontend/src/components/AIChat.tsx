"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Sparkles,
  Send,
  Loader2,
  Bot,
  User,
  Wrench,
  HelpCircle,
  Cpu,
} from "lucide-react";
import { askDatasetAI } from "../services/api";
import { ChatMessage } from "../types/dataset";

interface AIChatProps {
  datasetId: string;
  datasetName: string;
}

export const AIChat: React.FC<AIChatProps> = ({ datasetId, datasetName }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content: `Halo! Saya **DataMind AI Analyst**. Dataset **${datasetName}** telah selesai di-profiling. Silakan tanyakan apa saja seputar data ini, seperti statistik, missing values, distribusi, atau hubungan korelasi!`,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const starterPrompts = [
    "📊 Berikan ringkasan umum dataset ini",
    "🔍 Kolom mana yang memiliki missing values?",
    "📈 Berapa rata-rata dan nilai maksimum kolom numerik?",
    "🔗 Bagaimana korelasi antar variabel?",
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (questionText?: string) => {
    const question = (questionText || input).trim();
    if (!question || isLoading) return;

    setInput("");
    setError(null);

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: question,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await askDatasetAI(datasetId, question);
      const assistantMessage: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content: response.answer,
        tools_used: response.tools_used || [],
        model_used: response.model_used,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      const errorMessage =
        err.detail || err.message || "Gagal mendapatkan respons dari AI. Silakan coba lagi.";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Helper to render simple markdown-like formatting (bold, bullet points, code)
  const renderFormattedContent = (content: string) => {
    return content.split("\n").map((line, lIdx) => {
      // Bullet points
      if (line.trim().startsWith("* ") || line.trim().startsWith("- ")) {
        const text = line.trim().substring(2);
        return (
          <li key={lIdx} className="ml-4 list-disc text-slate-200">
            {formatInlineText(text)}
          </li>
        );
      }
      if (line.trim().startsWith("### ")) {
        return (
          <h5 key={lIdx} className="font-bold text-white text-sm mt-2 mb-1">
            {line.trim().substring(4)}
          </h5>
        );
      }
      if (line.trim() === "") {
        return <div key={lIdx} className="h-2" />;
      }
      return (
        <p key={lIdx} className="text-slate-200 mb-1 leading-relaxed">
          {formatInlineText(line)}
        </p>
      );
    });
  };

  const formatInlineText = (text: string) => {
    const parts = text.split(/(\*\*.*?\*\*|\*.*?\*|`.*?`)/g);
    return parts.map((part, pIdx) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={pIdx} className="font-bold text-white">
            {part.slice(2, -2)}
          </strong>
        );
      }
      if (part.startsWith("*") && part.endsWith("*")) {
        return (
          <em key={pIdx} className="italic text-indigo-300">
            {part.slice(1, -1)}
          </em>
        );
      }
      if (part.startsWith("`") && part.endsWith("`")) {
        return (
          <code
            key={pIdx}
            className="rounded bg-slate-800 px-1.5 py-0.5 font-mono text-xs text-indigo-300 border border-slate-700"
          >
            {part.slice(1, -1)}
          </code>
        );
      }
      return part;
    });
  };

  return (
    <div className="flex flex-col h-[650px] rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-md overflow-hidden shadow-2xl">
      {/* Chat Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800 bg-slate-950/60">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 shadow-md shadow-indigo-500/20 text-white">
            <Sparkles className="h-4 w-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="text-sm font-bold text-white">
                DataMind AI Assistant
              </h4>
              <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            </div>
            <p className="text-xs text-slate-400">
              Agent Tool Calling • Zero Numeric Hallucination
            </p>
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        {messages.map((msg) => {
          const isUser = msg.role === "user";
          return (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${
                isUser ? "flex-row-reverse" : "flex-row"
              }`}
            >
              <div
                className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-semibold ${
                  isUser
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "bg-slate-800 text-indigo-400 border border-slate-700"
                }`}
              >
                {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
              </div>

              <div
                className={`max-w-[85%] rounded-2xl px-4 py-3 text-xs sm:text-sm ${
                  isUser
                    ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/10"
                    : "bg-slate-950/80 border border-slate-800 text-slate-200 shadow-inner"
                }`}
              >
                <div className="space-y-1">{renderFormattedContent(msg.content)}</div>

                {/* Tools used & model meta */}
                {!isUser && (msg.tools_used?.length || msg.model_used) ? (
                  <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
                    {msg.model_used && (
                      <span className="flex items-center gap-1 text-slate-400 font-mono">
                        <Cpu className="h-3 w-3 text-indigo-400" />
                        {msg.model_used}
                      </span>
                    )}

                    {msg.tools_used && msg.tools_used.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className="text-slate-500">• Tools:</span>
                        {msg.tools_used.map((tool, tIdx) => (
                          <span
                            key={tIdx}
                            className="inline-flex items-center gap-1 rounded-md bg-indigo-500/10 px-2 py-0.5 font-mono text-[10px] text-indigo-300 border border-indigo-500/20"
                          >
                            <Wrench className="h-2.5 w-2.5" />
                            {tool}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ) : null}

                <div className="mt-1 text-[10px] text-slate-400 text-right">
                  {msg.timestamp}
                </div>
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-slate-800 text-indigo-400 border border-slate-700">
              <Bot className="h-4 w-4" />
            </div>
            <div className="rounded-2xl bg-slate-950/80 border border-slate-800 px-4 py-3 text-xs text-slate-300 flex items-center gap-2.5">
              <Loader2 className="h-4 w-4 animate-spin text-indigo-400" />
              <span>DataMind Analyst sedang menganalisis data & memanggil tool...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Starter Prompts */}
      <div className="px-4 py-2 border-t border-slate-800/60 bg-slate-950/40 overflow-x-auto flex items-center gap-2 scrollbar-none">
        {starterPrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(prompt)}
            disabled={isLoading}
            className="shrink-0 rounded-lg bg-slate-800/60 hover:bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:text-white border border-slate-700/60 transition-all active:scale-95 disabled:opacity-50 cursor-pointer"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Input */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/80">
        {error && (
          <p className="text-xs text-rose-400 mb-2 font-medium truncate">
            ⚠️ {error}
          </p>
        )}
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Tanyakan sesuatu tentang dataset ini... (contoh: Berapa rata-rata harganya?)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            className="flex-1 rounded-xl bg-slate-900 border border-slate-700 px-4 py-2.5 text-xs sm:text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all disabled:opacity-50"
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-md shadow-indigo-500/20 hover:from-indigo-600 hover:to-purple-700 active:scale-95 disabled:opacity-40 transition-all cursor-pointer"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
