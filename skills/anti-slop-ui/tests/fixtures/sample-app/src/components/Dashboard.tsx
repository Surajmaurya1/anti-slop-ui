import { useEffect, useState } from "react";

type Item = { id: string; title: string };

export default function Dashboard() {
  const [items, setItems] = useState<Item[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    fetch("/api/items").then((r) => r.json()).then(setItems);
  }, []);

  return (
    <section className="p-4">
      <button onClick={() => setOpen(!open)} className="border px-2 py-1">Toggle</button>
      {open && (
        <ul className="mt-2">
          {items.map((i) => (<li key={i.id}>{i.title}</li>))}
        </ul>
      )}
    </section>
  );
}
