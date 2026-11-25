import { useState } from "react";
import { Link } from "react-router-dom";

interface SignupFormProps {
  onSuccess: (email: string) => void;
  plan: "free" | "pro";
}

export function SignupForm({ onSuccess, plan }: SignupFormProps) {
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!/^\S+@\S+$/.test(email)) {
      setError("Enter a valid email");
      return;
    }
    setLoading(true);
    const res = await fetch("/api/signup", { method: "POST", body: JSON.stringify({ email, plan }) });
    setLoading(false);
    if (res.ok) onSuccess(email);
    else setError("Something went wrong");
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 p-4 border rounded">
      <label htmlFor="email" className="text-sm">Email</label>
      <input id="email" name="email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} className="border px-2 py-1" />
      {error && <p role="alert" className="text-red-600 text-sm">{error}</p>}
      <button type="submit" disabled={loading} className="bg-black text-white px-3 py-2 rounded">Sign up</button>
      <Link to="/login" className="text-sm underline">Already have an account?</Link>
    </form>
  );
}
