# AI_PROCESS.md

> **PLANTILLA — complétala tú.** Trycore evalúa que este documento sea honesto y escrito durante el trabajo, no después. Lo que está en MAYÚSCULAS entre corchetes `[...]` son marcas para que lo completes con tu experiencia real. Borra todas las instrucciones antes de entregar.

## 1. Herramientas de IA usadas y por qué

- **Claude (Anthropic)** — [EXPLICA con tus palabras por qué la elegiste]. 
- [AGREGA otras herramientas si las usaste: Copilot, ChatGPT, etc.]

**Declaración de transparencia:** [ESCRIBE exactamente qué generó la IA y qué hiciste tú. Por ejemplo: "El andamiaje inicial del backend, el frontend y los tests fue generado por Claude; yo lo revisé, lo ejecuté, modifiqué X, Y, Z y verifiqué los cálculos a mano". Sé específico y veraz.]

## 2. Prompts enviados (textuales y en orden cronológico)

> Copia aquí **todos** tus mensajes tal cual los escribiste, sin resumir ni corregir. Exporta o copia la conversación completa. Los dos primeros ya están; **agrega los siguientes en orden**.

**Prompt 1** (adjunto: PDF del desafío técnico de Trycore)

```
Ayudame a realizar esta solución y explicame los conceptosclaves de Valor ganado
```

**Prompt 2** (respuesta a la pregunta de Claude sobre el stack)

```
FastAPI + React (Recomendado)
```

[PROMPT 3...] 

## 3. Cómo aprendí EVM

[ESCRIBE qué le preguntaste a la IA, qué no entendías al principio y cómo validaste tu comprensión *antes* de usar el código. Ideas de validación que puedes haber hecho (cuenta solo las que hiciste de verdad):
- Resolver a mano los ejercicios de `docs/EVM_STUDY_GUIDE.md` y comparar con los tests.
- Explicar cada fórmula en voz alta sin mirar.
- Inventar un caso propio y predecir el resultado antes de ejecutarlo.
- Contrastar con una fuente externa (p. ej. guía PMI) y anotar diferencias.]

## 4. Dos decisiones donde NO seguí a la IA

> Deben ser decisiones reales tuyas. Al revisar el código, busca puntos donde tú elegirías distinto y documenta tu razonamiento. Si coincidiste con la IA en todo, dilo con honestidad y busca algo que sí cuestionarías.

### Decisión 1
- **Qué propuso la IA:** [...]
- **Qué hice yo y por qué:** [...]
- **Cómo verifiqué que mi camino era correcto:** [...]

### Decisión 2
- **Qué propuso la IA:** [...]
- **Qué hice yo y por qué:** [...]
- **Cómo verifiqué:** [...]

Puntos del código generado que podrías cuestionar (solo úsalos si de verdad estás en desacuerdo):
- Devolver `null` para CPI/SPI indefinidos vs. otra convención.
- Porcentajes en escala 0–100 vs. 0–1.
- Redondeo (4 decimales en índices, 2 en dinero).
- `PUT` con reemplazo completo vs. `PATCH` parcial.
- Estado "en presupuesto/cronograma" solo cuando el índice es exactamente 1 (sin tolerancia).

## 5. Cómo verifiqué que los cálculos son correctos

[Describe cómo comprobaste que **los números tienen sentido**, no solo que el código corre. Referencias disponibles en el repositorio:
- Caso del enunciado resuelto a mano (`docs/EVM_STUDY_GUIDE.md`, sección 4).
- Proyecto demo con resultado consolidado calculado a mano (`db/02_seed.sql` y `tests/integration/test_evm_report_api.py`).
- Propiedades de consistencia: EV = AC ⇒ CPI = 1; CPI < 1 ⇒ VAC < 0.
Agrega lo que hiciste tú.]

## 6. Una decisión de arquitectura tomada de forma independiente

[ESCRIBE una decisión que tomaste tú, sin que la IA la sugiriera: qué opciones había, por qué elegiste una y qué sacrificaste.]

## 7. Reflexión honesta: qué haría diferente

[ESCRIBE con sinceridad: qué te costó, dónde la IA se equivocó o fue poco útil, qué harías distinto si repitieras el ejercicio (por ejemplo, estudiar EVM antes de pedir código, escribir tú primero los tests de casos borde, comprometer el historial de Git más gradualmente, etc.).]
