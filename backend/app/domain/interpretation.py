"""Human-readable interpretation of CPI and SPI statuses."""

from app.domain.status import CostStatus, ScheduleStatus

COST_MESSAGES: dict[CostStatus, str] = {
    CostStatus.UNDER_BUDGET: "Bajo presupuesto: se obtiene más valor por cada peso gastado.",
    CostStatus.ON_BUDGET: "En presupuesto: el gasto coincide con el avance logrado.",
    CostStatus.OVER_BUDGET: "Sobre presupuesto: se está gastando más de lo que se avanza.",
    CostStatus.UNDEFINED: "Sin datos de costo: no hay costo real registrado para calcular el CPI.",
}

SCHEDULE_MESSAGES: dict[ScheduleStatus, str] = {
    ScheduleStatus.AHEAD: "Adelantado: el avance real supera lo planificado.",
    ScheduleStatus.ON_SCHEDULE: "En cronograma: el avance real coincide con lo planificado.",
    ScheduleStatus.BEHIND: "Atrasado: el avance real está por debajo de lo planificado.",
    ScheduleStatus.UNDEFINED: "Sin avance planificado: no hay valor planificado para el SPI.",
}
