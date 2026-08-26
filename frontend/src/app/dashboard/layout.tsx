"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/");
    }
  }, [router]);

  if (!mounted) return null;

  return (
    <div className="flex min-h-screen flex-col bg-gray-50 text-gray-900">
      <header className="sticky top-0 z-10 border-b bg-white px-4 py-3 shadow-sm">
        <div className="mx-auto flex max-w-5xl items-center justify-between">
          <Link href="/dashboard" className="text-xl font-bold text-blue-600">
            SEO Expert
          </Link>
          <nav className="space-x-4 hidden md:block">
            <Link href="/dashboard" className="text-sm font-medium hover:text-blue-600">Dashboard</Link>
            <Link href="/dashboard/chat" className="text-sm font-medium hover:text-blue-600">AI Chat</Link>
          </nav>
          <button 
            onClick={() => {
              localStorage.removeItem("token");
              router.push("/");
            }}
            className="text-sm font-medium text-red-600 hover:underline"
          >
            Logout
          </button>
        </div>
      </header>
      
      <main className="mx-auto w-full max-w-5xl flex-1 p-4">
        {children}
      </main>

      {/* Mobile Bottom Navigation (Mobile-first requirement) */}
      <nav className="sticky bottom-0 border-t bg-white p-3 flex justify-around md:hidden">
        <Link href="/dashboard" className="text-sm font-medium text-blue-600 flex flex-col items-center">
          <span>📊</span>
          <span>Home</span>
        </Link>
        <Link href="/dashboard/tasks" className="text-sm font-medium text-gray-500 flex flex-col items-center">
          <span>✅</span>
          <span>Tasks</span>
        </Link>
        <Link href="/dashboard/chat" className="text-sm font-medium text-gray-500 flex flex-col items-center">
          <span>🤖</span>
          <span>AI Chat</span>
        </Link>
      </nav>
    </div>
  );
}
