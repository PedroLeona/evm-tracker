# Guía de estudio: Valor Ganado (EVM)

Úsala para prepararte para el video: tienes que explicar el EVM **con tus palabras, sin leer**. Practica contestando cada pregunta en voz alta antes de mirar la respuesta.

## 1. La idea en una frase

Gastar y avanzar no se pueden juzgar por separado: lo que importa es la relación. Para compararlos se convierte todo a **dinero**: el avance se valora a precio de presupuesto.

## 2. Los tres valores base

| Sigla | Nombre | Pregunta | Cálculo |
|---|---|---|---|
| BAC | Presupuesto total | ¿Cuánto cuesta todo el trabajo según el plan? | dato |
| PV | Valor planificado | ¿Cuánto trabajo *debería* llevar hecho hoy? | % planificado × BAC |
| EV | Valor ganado | ¿Cuánto trabajo *llevo realmente* hecho? | % real × BAC |
| AC | Costo real | ¿Cuánto he gastado? | dato |

## 3. Variaciones e índices

- **CV = EV − AC** (en dinero): negativo = gasté más de lo que valía lo avanzado.
- **SV = EV − PV** (en dinero): negativo = llevo menos trabajo del que debía.
- **CPI = EV / AC** (ratio): por cada $1 gastado, ¿cuánto valor produje? 0,85 → 85 centavos.
- **SPI = EV / PV** (ratio): ¿qué fracción de lo planeado he hecho? 0,80 → voy al 80 % del ritmo.
- **EAC = BAC / CPI**: costo final proyectado si la eficiencia actual no cambia.
- **VAC = BAC − EAC**: diferencia final proyectada; negativo = sobrecosto.

> **Variación vs índice:** la variación dice *cuánto* (en dinero); el índice dice *qué proporción*. Un CV de −1.000 es grave en un proyecto de 5.000 y trivial en uno de 5 millones; el CPI sí es comparable entre proyectos.

## 4. Ejemplo resuelto a mano (el del enunciado)

BAC = 1.000, plan 50 %, real 40 %, AC = 600.

1. PV = 0,50 × 1.000 = **500**
2. EV = 0,40 × 1.000 = **400**
3. CV = 400 − 600 = **−200** → sobrecosto
4. SV = 400 − 500 = **−100** → atrasado
5. CPI = 400 / 600 = **0,6667** → rinde 67 centavos por peso
6. SPI = 400 / 500 = **0,80**
7. EAC = 1.000 / 0,6667 = **1.500**
8. VAC = 1.000 − 1.500 = **−500** → terminará 500 por encima del presupuesto

## 5. Ejercicios (resuelve a mano y compara)

1. BAC 2.000, plan 30 %, real 30 %, AC 500. ¿Cuánto vale cada indicador? ¿Cómo está el proyecto?
2. BAC 10.000, plan 80 %, real 60 %, AC 5.000. Observa: gastas poco, pero ¿vas bien? (Pista: mira el SPI.)
3. Un proyecto con dos actividades: A (BAC 100, EV 100, AC 50) y B (BAC 900, EV 450, AC 900). Calcula el CPI consolidado con sumas y luego promediando los CPI de A y B. ¿Por qué difieren? ¿Cuál es el correcto?

<details>
<summary>Respuestas</summary>

1. PV = 600, EV = 600, AC = 500, CV = +100, SV = 0, CPI = 1,20, SPI = 1,00, EAC = 1.666,67, VAC = +333,33. Bajo presupuesto y en cronograma.
2. PV = 8.000, EV = 6.000, AC = 5.000, CV = +1.000, SV = −2.000, CPI = 1,20, SPI = 0,75. Eficiente en costo pero atrasado: gastar poco *no* es buena señal si no avanzas.
3. Consolidado: EV 550 / AC 950 = **0,579**. Promedio de índices: (2,0 + 0,5) / 2 = 1,25, engañoso. Es correcto sumar: B pesa 9 veces más en presupuesto y es el que va mal.
</details>

## 6. Casos borde (decisiones que tendrás que explicar)

| Caso | Qué pasa | Decisión tomada |
|---|---|---|
| AC = 0 | CPI = EV/0 | CPI `null`, EAC/VAC `null` |
| PV = 0 | SPI = EV/0 | SPI `null` |
| EV = 0 y AC > 0 | CPI = 0 | CPI 0 (sobrecosto) y EAC `null` (infinito) |
| Sin actividades | todo en 0 | índices `null`, estado "sin datos" |

Pregúntate: ¿por qué `null` y no 0 o 1? (Porque 0 significaría "muy mal", 1 "perfecto", y en realidad no hay datos.)

## 7. Cómo verificar que los números tienen sentido

- Si EV = AC → CPI debe ser exactamente 1.
- Si EV = PV → SPI debe ser exactamente 1.
- Si CPI < 1 → EAC > BAC y VAC < 0 (siempre deben ir de la mano).
- Si la actividad está 100 % completada → EAC debe ser igual a AC.
- El consolidado debe coincidir con calcular los totales a mano.

## 8. Guion sugerido para el video (≤ 10 min)

1. **EVM en tus palabras (2–3 min):** el problema "gasté 60 % y avancé 40 %" y cómo EV lo resuelve; ejemplo con números.
2. **Arquitectura (2 min):** capas, por qué el dominio es puro.
3. **Una decisión difícil (1–2 min):** p. ej. consolidar sumando vs promediando, o qué devolver cuando el denominador es 0.
4. **Demo (2–3 min):** un proyecto, tres actividades, cambia un dato y mira cómo se actualizan semáforo y gráfica.
5. **Flujo con IA (1–2 min):** muestra `AI_PROCESS.md`.
