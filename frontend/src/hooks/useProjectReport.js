import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client.js";

export function useProjectReport(projectId) {
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const reload = useCallback(async () => {
    if (projectId == null) {
      setReport(null);
      return;
    }
    try {
      setReport(await api.getReport(projectId));
      setError(null);
    } catch (caught) {
      setError(caught.message);
    }
  }, [projectId]);

  useEffect(() => {
    reload();
  }, [reload]);

  const saveActivity = async (activityId, payload) => {
    if (activityId == null) await api.createActivity(projectId, payload);
    else await api.updateActivity(activityId, payload);
    await reload();
  };

  const removeActivity = async (activityId) => {
    await api.deleteActivity(activityId);
    await reload();
  };

  return { report, error, saveActivity, removeActivity };
}
