const BASE_URL = "http://localhost:8000"; // ✅ match your API port

export const getLogs = async () => {
  const response = await fetch(BASE_URL);
  if (!response.ok) throw new Error("Failed to fetch logs");
  const data = await response.json();
  console.log("Fetched logs:", data); // ✅ This should now log an array
  return data; // ✅ data is a plain array, not { results: [...] }
};


export const getFilters = async () => {
    const response = await fetch(`${BASE_URL}/filters`)
    const data = await response.json();
    if (!response.ok) throw new Error("Failed to fetch logs");
    return data;
}
