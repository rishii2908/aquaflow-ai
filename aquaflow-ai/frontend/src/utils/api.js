const BASE = import.meta.env.VITE_API_URL || "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json();
}

export const api = {
  getSensors: () => request("/sensors/"),
  getSensor: (id) => request(`/sensors/${id}`),
  getReadings: (id, limit = 60) => request(`/sensors/${id}/readings?limit=${limit}`),
  ingestReading: (id, data) => request(`/sensors/${id}/readings`, { method: "POST", body: JSON.stringify(data) }),

  getAnomalies: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/anomalies/${q ? "?" + q : ""}`);
  },

  getAlerts: (unacknowledgedOnly = false) =>
    request(`/alerts/${unacknowledgedOnly ? "?unacknowledged_only=true" : ""}`),
  acknowledgeAlert: (id, operatorName) =>
    request(`/alerts/${id}/acknowledge`, {
      method: "POST",
      body: JSON.stringify({ operator_name: operatorName }),
    }),

  getSummary: () => request("/reports/summary"),
};
