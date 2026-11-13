import { useState } from "react";
import ActivityForm from "./components/ActivityForm.jsx";
import ActivityTable from "./components/ActivityTable.jsx";
import EvmChart from "./components/EvmChart.jsx";
import KpiPanel from "./components/KpiPanel.jsx";
import ProjectBar from "./components/ProjectBar.jsx";
import { useProjectReport } from "./hooks/useProjectReport.js";
import { useProjects } from "./hooks/useProjects.js";

const DELETE_PROJECT_CONFIRMATION = "¿Eliminar el proyecto y todas sus actividades?";
const DELETE_ACTIVITY_CONFIRMATION = "¿Eliminar esta actividad?";

export default function App() {
  const projectsState = useProjects();
  const { report, error: reportError, saveActivity, removeActivity } = useProjectReport(
    projectsState.selectedProjectId,
  );
  const [editingActivity, setEditingActivity] = useState(null);

  const handleSubmitActivity = async (payload) => {
    await saveActivity(editingActivity?.id ?? null, payload);
    setEditingActivity(null);
  };

  const handleDeleteActivity = async (activity) => {
    if (!window.confirm(DELETE_ACTIVITY_CONFIRMATION)) return;
    await removeActivity(activity.id);
    if (editingActivity?.id === activity.id) setEditingActivity(null);
  };

  const handleDeleteProject = async (projectId) => {
    if (!window.confirm(DELETE_PROJECT_CONFIRMATION)) return;
    await projectsState.deleteProject(projectId);
    setEditingActivity(null);
  };

  const handleSelectProject = (projectId) => {
    setEditingActivity(null);
    projectsState.setSelectedProjectId(projectId);
  };

  const visibleError = projectsState.error ?? reportError;

  return (
    <main>
      <h1>EVM Tracker · Valor Ganado</h1>
      {visibleError && <p className="error">{visibleError}</p>}

      <ProjectBar
        projects={projectsState.projects}
        selectedProjectId={projectsState.selectedProjectId}
        onSelect={handleSelectProject}
        onCreate={projectsState.createProject}
        onDelete={handleDeleteProject}
      />

      {report && (
        <>
          <KpiPanel consolidated={report.consolidated} />
          <EvmChart activities={report.activities} />
          <ActivityTable
            activities={report.activities}
            onEdit={setEditingActivity}
            onDelete={handleDeleteActivity}
          />
          <ActivityForm
            key={editingActivity?.id ?? "new"}
            editingActivity={editingActivity}
            onSubmit={handleSubmitActivity}
            onCancel={() => setEditingActivity(null)}
          />
        </>
      )}
    </main>
  );
}
