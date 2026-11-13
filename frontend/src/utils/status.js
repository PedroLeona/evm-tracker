export const TONE = {
  GOOD: "good",
  BAD: "bad",
  NEUTRAL: "neutral",
};

const COST_STATUS_VIEW = {
  UNDER_BUDGET: { label: "Bajo presupuesto", tone: TONE.GOOD },
  ON_BUDGET: { label: "En presupuesto", tone: TONE.GOOD },
  OVER_BUDGET: { label: "Sobre presupuesto", tone: TONE.BAD },
  UNDEFINED: { label: "Sin datos", tone: TONE.NEUTRAL },
};

const SCHEDULE_STATUS_VIEW = {
  AHEAD: { label: "Adelantado", tone: TONE.GOOD },
  ON_SCHEDULE: { label: "En cronograma", tone: TONE.GOOD },
  BEHIND: { label: "Atrasado", tone: TONE.BAD },
  UNDEFINED: { label: "Sin datos", tone: TONE.NEUTRAL },
};

export const costStatusView = (status) => COST_STATUS_VIEW[status];
export const scheduleStatusView = (status) => SCHEDULE_STATUS_VIEW[status];

export function overallTone(costStatus, scheduleStatus) {
  const tones = [costStatusView(costStatus).tone, scheduleStatusView(scheduleStatus).tone];
  if (tones.includes(TONE.BAD)) return TONE.BAD;
  if (tones.every((tone) => tone === TONE.NEUTRAL)) return TONE.NEUTRAL;
  return TONE.GOOD;
}

const OVERALL_HEADLINES = {
  [TONE.GOOD]: "El proyecto va bien",
  [TONE.BAD]: "El proyecto necesita atención",
  [TONE.NEUTRAL]: "Aún no hay datos suficientes",
};

export const overallHeadline = (tone) => OVERALL_HEADLINES[tone];
