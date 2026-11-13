import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client.js";

export function useProjects() {
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    try {
      const loaded = await api.listProjects();
      setProjects(loaded);
      setSelectedProjectId((current) => {
        const stillExists = loaded.some((project) => project.id === current);
        return stillExists ? current : (loaded[0]?.id ?? null);
      });
    } catch (caught) {
      setError(caught.message);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const createProject = async (payload) => {
    const created = await api.createProject(payload);
    await refresh();
    setSelectedProjectId(created.id);
  };

  const deleteProject = async (projectId) => {
    await api.deleteProject(projectId);
    await refresh();
  };

  return {
    projects,
    selectedProjectId,
    setSelectedProjectId,
    createProject,
    deleteProject,
    error,
  };
}
