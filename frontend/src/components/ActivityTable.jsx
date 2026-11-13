import { formatIndex, formatMoney, formatPercent } from "../utils/formatters.js";
import { costStatusView, scheduleStatusView } from "../utils/status.js";
import StatusBadge from "./StatusBadge.jsx";

const HEADERS = [
  "Actividad", "BAC", "% plan", "% real", "AC", "PV", "EV",
  "CV", "SV", "CPI", "SPI", "EAC", "VAC", "",
];

function ActivityRow({ activity, onEdit, onDelete }) {
  const { metrics } = activity;
  return (
    <tr>
      <td>{activity.name}</td>
      <td>{formatMoney(activity.budget_at_completion)}</td>
      <td>{formatPercent(activity.planned_percent)}</td>
      <td>{formatPercent(activity.actual_percent)}</td>
      <td>{formatMoney(activity.actual_cost)}</td>
      <td>{formatMoney(metrics.planned_value)}</td>
      <td>{formatMoney(metrics.earned_value)}</td>
      <td className={metrics.cost_variance < 0 ? "negative" : ""}>{formatMoney(metrics.cost_variance)}</td>
      <td className={metrics.schedule_variance < 0 ? "negative" : ""}>{formatMoney(metrics.schedule_variance)}</td>
      <td>
        {formatIndex(metrics.cost_performance_index)}{" "}
        <StatusBadge view={costStatusView(metrics.cost_status)} title={metrics.cost_interpretation} />
      </td>
      <td>
        {formatIndex(metrics.schedule_performance_index)}{" "}
        <StatusBadge view={scheduleStatusView(metrics.schedule_status)} title={metrics.schedule_interpretation} />
      </td>
      <td>{formatMoney(metrics.estimate_at_completion)}</td>
      <td>{formatMoney(metrics.variance_at_completion)}</td>
      <td className="actions">
        <button type="button" onClick={() => onEdit(activity)}>Editar</button>
        <button type="button" className="danger" onClick={() => onDelete(activity)}>Eliminar</button>
      </td>
    </tr>
  );
}

export default function ActivityTable({ activities, onEdit, onDelete }) {
  return (
    <section className="panel">
      <h2>Actividades</h2>
      {activities.length === 0 ? (
        <p className="muted">Este proyecto aún no tiene actividades.</p>
      ) : (
        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                {HEADERS.map((header, index) => (
                  <th key={`${header}-${index}`}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {activities.map((activity) => (
                <ActivityRow key={activity.id} activity={activity} onEdit={onEdit} onDelete={onDelete} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
