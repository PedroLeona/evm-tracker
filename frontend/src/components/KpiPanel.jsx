import { formatIndex, formatMoney } from "../utils/formatters.js";
import {
  costStatusView,
  overallHeadline,
  overallTone,
  scheduleStatusView,
} from "../utils/status.js";
import StatusBadge from "./StatusBadge.jsx";

function Kpi({ label, hint, value, tone }) {
  return (
    <div className={`kpi ${tone ? `kpi--${tone}` : ""}`}>
      <span className="kpi__label" title={hint}>
        {label}
      </span>
      <span className="kpi__value">{value}</span>
    </div>
  );
}

const signedTone = (value) => (value < 0 ? "bad" : "good");

export default function KpiPanel({ consolidated }) {
  const costView = costStatusView(consolidated.cost_status);
  const scheduleView = scheduleStatusView(consolidated.schedule_status);
  const tone = overallTone(consolidated.cost_status, consolidated.schedule_status);

  return (
    <section className="panel">
      <div className={`headline headline--${tone}`}>
        <h2>{overallHeadline(tone)}</h2>
        <p className="muted">
          Tolerancia aplicada: ±{consolidated.tolerance_percent}% (un índice dentro de ese rango
          se considera &quot;en plan&quot;)
        </p>
        <div className="headline__statuses">
          <div>
            <strong>Costo (CPI {formatIndex(consolidated.cost_performance_index)})</strong>
            <StatusBadge view={costView} />
            <p>{consolidated.cost_interpretation}</p>
          </div>
          <div>
            <strong>Cronograma (SPI {formatIndex(consolidated.schedule_performance_index)})</strong>
            <StatusBadge view={scheduleView} />
            <p>{consolidated.schedule_interpretation}</p>
          </div>
        </div>
      </div>

      <div className="kpi-grid">
        <Kpi label="BAC" hint="Presupuesto total" value={formatMoney(consolidated.budget_at_completion)} />
        <Kpi label="PV" hint="Valor planificado" value={formatMoney(consolidated.planned_value)} />
        <Kpi label="EV" hint="Valor ganado" value={formatMoney(consolidated.earned_value)} />
        <Kpi label="AC" hint="Costo real" value={formatMoney(consolidated.actual_cost)} />
        <Kpi
          label="CV"
          hint="Variación de costo (EV - AC)"
          value={formatMoney(consolidated.cost_variance)}
          tone={signedTone(consolidated.cost_variance)}
        />
        <Kpi
          label="SV"
          hint="Variación de cronograma (EV - PV)"
          value={formatMoney(consolidated.schedule_variance)}
          tone={signedTone(consolidated.schedule_variance)}
        />
        <Kpi label="EAC" hint="Estimado al terminar (BAC / CPI)" value={formatMoney(consolidated.estimate_at_completion)} />
        <Kpi
          label="VAC"
          hint="Variación al terminar (BAC - EAC)"
          value={formatMoney(consolidated.variance_at_completion)}
          tone={consolidated.variance_at_completion == null ? undefined : signedTone(consolidated.variance_at_completion)}
        />
      </div>
    </section>
  );
}
