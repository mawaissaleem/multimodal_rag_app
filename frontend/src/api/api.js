const API_BASE = "http://localhost:8000"; // Change if needed

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Upload failed");
  return await res.json();
}

export async function sendQuery(question) {
  const res = await fetch(`${API_BASE}/query/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: question,
      filename: null,
      top_k: 5
    }),
  });

  const json = await res.json();
  console.log("Received from backend:", json);

  if (!res.ok) throw new Error("Query failed");
  
  // Map backend response to frontend expected format
  return {
    answer: json.generated_answer,
    sources: json.results || []
  };
}