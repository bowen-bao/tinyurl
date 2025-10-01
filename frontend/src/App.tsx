// frontend/src/App.tsx
import { useState } from "react";

export default function App() {
  const [url, setUrl] = useState("");
  const [short, setShort] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function onShorten(e: React.FormEvent) {
    e.preventDefault();
    setErr(null); setShort(null);
    try {
      const res = await fetch("http://bowenbao.com/api/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      setShort(`http://bowenbao.com${data.shortUrl}`);
    } catch (e: any) {
      setErr(e.message);
    }
  }

  return (
    <div style={{ maxWidth: 560, margin: "4rem auto", fontFamily: "sans-serif" }}>
      <h1>tinyurl (mvp)</h1>
      <form onSubmit={onShorten}>
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="paste a long URL"
          style={{ width: "100%", padding: 12, fontSize: 16 }}
        />
        <button style={{ marginTop: 12, padding: "10px 16px" }}>Shorten</button>
      </form>
      {short && <p>short URL: <a href={short}>{short}</a></p>}
      {err && <p style={{ color: "crimson" }}>{err}</p>}
    </div>
  );
}

