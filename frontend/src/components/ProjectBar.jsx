import { useState } from "react";

export default function ProjectBar({
  projects,
  selectedProjectId,
  onSelect,
  onCreate,
  onDelete,
}) {
  const [newName, setNewName] = useState("");
  const [error, setError] = useState(null);

  const handleCreate = async (event) => {
    event.preventDefault();
    try {
      await onCreate({ name: newName.trim(), description: null });
      setNewName("");
      setError(null);
    } catch (caught) {
      setError(caught.message);
    }
  };

  return (
    <section className="panel project-bar">
      <label>
        Proyecto
        <select
          value={selectedProjectId ?? ""}
          onChange={(event) => onSelect(Number(event.target.value))}
          disabled={projects.length === 0}
        >
          {projects.length === 0 && <option value="">Sin proyectos</option>}
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>
      </label>
      {selectedProjectId != null && (
        <button type="button" className="danger" onClick={() => onDelete(selectedProjectId)}>
          Eliminar proyecto
        </button>
      )}
      <form onSubmit={handleCreate} className="project-bar__new">
        <input
          required
          placeholder="Nombre del nuevo proyecto"
          value={newName}
          onChange={(event) => setNewName(event.target.value)}
        />
        <button type="submit">Crear proyecto</button>
      </form>
      {error && <p className="error">{error}</p>}
    </section>
  );
}
