import { useState } from "react";

const EMPTY_FORM = {
  name: "",
  budget_at_completion: "",
  planned_percent: "",
  actual_percent: "",
  actual_cost: "",
};

const NUMERIC_FIELDS = ["budget_at_completion", "planned_percent", "actual_percent", "actual_cost"];

const FIELDS = [
  { key: "name", label: "Nombre", type: "text" },
  { key: "budget_at_completion", label: "Presupuesto total (BAC)", type: "number", min: 0, step: "0.01" },
  { key: "planned_percent", label: "% avance planificado", type: "number", min: 0, max: 100, step: "0.01" },
  { key: "actual_percent", label: "% avance real", type: "number", min: 0, max: 100, step: "0.01" },
  { key: "actual_cost", label: "Costo real (AC)", type: "number", min: 0, step: "0.01" },
];

function toForm(activity) {
  if (!activity) return EMPTY_FORM;
  return Object.fromEntries(Object.keys(EMPTY_FORM).map((key) => [key, String(activity[key])]));
}

function toPayload(form) {
  const payload = { ...form };
  NUMERIC_FIELDS.forEach((key) => {
    payload[key] = Number(form[key]);
  });
  return payload;
}

export default function ActivityForm({ editingActivity, onSubmit, onCancel }) {
  const [form, setForm] = useState(() => toForm(editingActivity));
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (key) => (event) => setForm({ ...form, [key]: event.target.value });

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit(toPayload(form));
      setForm(EMPTY_FORM);
      setError(null);
    } catch (caught) {
      setError(caught.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="panel">
      <h2>{editingActivity ? "Editar actividad" : "Nueva actividad"}</h2>
      <form className="activity-form" onSubmit={handleSubmit}>
        {FIELDS.map(({ key, label, ...inputProps }) => (
          <label key={key}>
            {label}
            <input required value={form[key]} onChange={handleChange(key)} {...inputProps} />
          </label>
        ))}
        <div className="form-actions">
          <button type="submit" disabled={submitting}>
            {editingActivity ? "Guardar cambios" : "Agregar actividad"}
          </button>
          {editingActivity && (
            <button type="button" className="secondary" onClick={onCancel}>
              Cancelar
            </button>
          )}
        </div>
      </form>
      {error && <p className="error">{error}</p>}
    </section>
  );
}
