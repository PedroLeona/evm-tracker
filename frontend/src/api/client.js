const API_BASE_URL = import.meta.env.VITE_API_URL ?? "/api";
const HTTP_NO_CONTENT = 204;
const GENERIC_ERROR_MESSAGE = "No se pudo completar la solicitud";

async function extractErrorMessage(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) {
      return body.detail.map((issue) => `${issue.loc.slice(1).join(".")}: ${issue.msg}`).join("; ");
    }
  } catch {
    return GENERIC_ERROR_MESSAGE;
  }
  return GENERIC_ERROR_MESSAGE;
}

async function request(path, { method = "GET", body } = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) throw new Error(await extractErrorMessage(response));
  return response.status === HTTP_NO_CONTENT ? null : response.json();
}

export const api = {
  listProjects: () => request("/projects"),
  createProject: (payload) => request("/projects", { method: "POST", body: payload }),
  deleteProject: (projectId) => request(`/projects/${projectId}`, { method: "DELETE" }),
  getReport: (projectId) => request(`/projects/${projectId}/evm`),
  createActivity: (projectId, payload) =>
    request(`/projects/${projectId}/activities`, { method: "POST", body: payload }),
  updateActivity: (activityId, payload) =>
    request(`/activities/${activityId}`, { method: "PUT", body: payload }),
  deleteActivity: (activityId) => request(`/activities/${activityId}`, { method: "DELETE" }),
};
