import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatMoney } from "../utils/formatters.js";

const CHART_HEIGHT = 320;
const SERIES = [
  { key: "PV", label: "PV (planificado)", color: "#5b8def" },
  { key: "EV", label: "EV (ganado)", color: "#2e9e6b" },
  { key: "AC", label: "AC (costo real)", color: "#e0623c" },
];

export default function EvmChart({ activities }) {
  const data = activities.map((activity) => ({
    name: activity.name,
    PV: activity.metrics.planned_value,
    EV: activity.metrics.earned_value,
    AC: activity.metrics.actual_cost,
  }));

  return (
    <section className="panel">
      <h2>PV, EV y AC por actividad</h2>
      {data.length === 0 ? (
        <p className="muted">Agrega actividades para ver la gráfica.</p>
      ) : (
        <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip formatter={(value) => formatMoney(value)} />
            <Legend />
            {SERIES.map((series) => (
              <Bar key={series.key} dataKey={series.key} name={series.label} fill={series.color} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      )}
    </section>
  );
}
