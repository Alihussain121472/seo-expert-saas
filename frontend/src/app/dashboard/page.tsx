"use client";

import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";

type Website = {
  id: string;
  url: string;
  name: string;
};

export default function DashboardPage() {
  const [websites, setWebsites] = useState<Website[]>([]);
  const [loading, setLoading] = useState(true);
  const [newUrl, setNewUrl] = useState("");
  const [newName, setNewName] = useState("");

  const loadWebsites = async () => {
    try {
      const data = await fetchAPI("/websites");
      setWebsites(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWebsites();
  }, []);

  const handleAddWebsite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUrl) return;
    
    try {
      await fetchAPI("/websites", {
        method: "POST",
        body: JSON.stringify({ url: newUrl, name: newName }),
      });
      setNewUrl("");
      setNewName("");
      loadWebsites();
    } catch (err) {
      console.error(err);
      alert("Failed to add website");
    }
  };

  if (loading) return <div className="text-center p-10">Loading...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Your Websites</h1>

      {websites.length === 0 ? (
        <div className="rounded-xl border border-dashed border-gray-300 bg-white p-10 text-center shadow-sm">
          <h2 className="text-lg font-semibold text-gray-700">No websites connected yet</h2>
          <p className="mt-2 text-sm text-gray-500">Connect your first website to start the AI SEO Audit.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {websites.map((site) => (
            <div key={site.id} className="rounded-xl border bg-white p-5 shadow-sm transition hover:shadow-md">
              <h3 className="font-semibold text-lg truncate">{site.name || site.url}</h3>
              <p className="text-sm text-gray-500 truncate">{site.url}</p>
              
              <div className="mt-4 flex items-center justify-between">
                <span className="inline-flex items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800">
                  Audit Pending
                </span>
                <button className="text-sm font-medium text-blue-600 hover:underline">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-8 rounded-xl border bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">Connect New Website</h2>
        <form onSubmit={handleAddWebsite} className="space-y-4 sm:flex sm:space-y-0 sm:space-x-4">
          <div className="flex-1">
            <input
              type="url"
              placeholder="https://example.com"
              value={newUrl}
              onChange={(e) => setNewUrl(e.target.value)}
              className="w-full rounded-md border border-gray-300 p-2 text-black shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
          <div className="flex-1">
            <input
              type="text"
              placeholder="Website Name (Optional)"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              className="w-full rounded-md border border-gray-300 p-2 text-black shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="w-full sm:w-auto rounded-md bg-blue-600 px-4 py-2 text-white font-medium hover:bg-blue-700"
          >
            Connect
          </button>
        </form>
      </div>
    </div>
  );
}
