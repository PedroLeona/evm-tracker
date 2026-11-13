# AI_PROCESS.md

## 1. Herramientas de inteligencia artificial utilizadas

Durante el desarrollo del reto se utilizaron **Claude** y **ChatGPT** como herramientas de apoyo. Las respuestas generadas fueron revisadas y contrastadas con la implementación, las pruebas y los resultados obtenidos.

## 2. Uso de ChatGPT

No se conserva en este documento una transcripción literal y completa de todos los prompts enviados a ChatGPT. Por transparencia, se describe el propósito de las consultas realizadas, sin presentar estas descripciones como prompts textuales.

Las consultas a ChatGPT se utilizaron principalmente para:

1. **Organización y priorización del trabajo:** revisar los entregables pendientes y mantener el foco en pruebas, Docker, frontend, Swagger, Gitflow y documentación.
2. **Comprensión y validación de EVM:** aclarar conceptos de Valor Ganado y practicar con escenarios hipotéticos para comprender PV, EV, AC, CV, SV, CPI, SPI, EAC y VAC.
3. **Validación de interpretaciones:** analizar los resultados de ejercicios, la diferencia entre el CPI consolidado y el promedio de CPI individuales, y los casos en los que una división por cero impide determinar un indicador.
4. **Revisión de reglas de negocio:** discutir el efecto del redondeo en indicadores cercanos a 1 y evaluar tolerancias configurables según el BAC.
5. **Revisión de la entrega:** verificar resultados de pruebas, cobertura, compilación del frontend y pasos de Gitflow; además de organizar la sustentación y este documento.

En algunos momentos fue necesario redirigir la conversación para evitar profundizar en temas que no eran prioritarios para completar el reto.

## 3. Consultas realizadas a Claude

Se registran los prompts de Claude que se lograron recuperar. Se conserva su redacción original, incluidos errores tipográficos. Los dos registros del prompt sobre tolerancia corresponden a dos envíos distintos.

| Orden | Fecha y hora | Prompt enviado |
|---:|---|---|
| 1 | 12 nov., 17:23 | `Ayudame a realizar esta solución y explicame los conceptosclaves de Valor ganado` |
| 2 | Durante la selección de tecnología | `FastAPI + React (Recomendado)` |
| 3 | 12 nov., 17:37 | `Quiero saber que elementos necesito para poder probar el proyecto y partir de ahi poder hacer una pruebo y luego si me gustaria entender la solucion mas a detalle` |
| 4 | 12 nov., 17:39 | `Tengo instalado docker` |
| 5 | 13 nov., 09:10 | `ya cargo, como edito Development?` |
| 6 | 13 nov., 09:13 | `Crea un documento de Word a partir de tu última respuesta.` |
| 7 | 13 nov., 09:16 | `listo si dieron los datos y al cambiarlo volvio a salir CPI 0,85 y SPI 0,82` |
| 8 | 13 nov., 09:17 | `No, Primero quiero entender la logica del Valor Ganado y hacer pruebas para validar el conocimiento` |
| 9 | 13 nov., 09:28 | `no entiendo de de donde sale AC` |
| 10 | 13 nov., 09:40 | `PV=600,EV=600,CV=100,SV=0,CPI=1.2,SPI=1\n\nentiendo que con eso datos lo que quiere decir esq que el proyecto va de acuerdo al plan en cuanto a tiempo y gasto?` |
| 11 | 13 nov., 09:56 | `CV=1000,sv=-2000,cpi=1.2,spi=0.75\n\nentendiendo los valores de cpi y spi, podria concluir que en cuando al gasto es positivo ya que se estaria ahorrando 1000 y en cuanto al tiempo si estaria retrasado un 25%` |
| 12 | 13 nov., 10:23 | `A EV=100,CPI=2\nB EV=450, CPI=0.5\nCPIsumado 0.57\nPromedio CPI 1.25\n\nla actividad que mas pesas es la B ya que segun los numeros esta ya consumio el presupuesto y esta en la mitad del proyecto, la A ya termino y tuvo un ahorro de la mitad pero esta seria absrobida por la sedunda actividad` |
| 13 | 13 nov., 10:34 | `1. entiendo que en ese caso no se podria determinar bien ya que no tendria ninguna avance por el momento\n2. En estos casos que la operacion puede generar error si se divide entre 0, se deberia mostrar un mensaje que diga que no se puede determinar\n3. No se` |
| 14 | 13 nov., 10:38 | `Opcion B` |
| 15 | 13 nov., 11:03 | `entiendo que si se redondiara 0.99996 este podria ser interpretado como 1, pero en realidad existe una pequeña diferencia que podrian suponer pequeñas perdidas` |
| 16 | 13 nov., 11:05 | `yo manejaria un nivel de toleracia pero dependiendo del BAC ya que este porcentaje puede significar diferencia dependiendo ese presupuesto` |
| 17 | 13 nov., 11:10 | `me parece bien por el momento manejar esos umbrales, pero dejar que se puedan modificar en el futuro sabiendo que depronto personas del negocio o proyecto pueden tener mejor contexto y delimitar mas estos niveles` |
| 18 | 13 nov., 16:02 | `me parece bien por el momento manejar esos umbrales, pero dejar que se puedan modificar en el futuro sabiendo que depronto personas del negocio o proyecto pueden tener mejor contexto y delimitar mas estos niveles` |
| 19 | 13 nov., 17:21 | `tu me puedes entregar los prompts que hice en orden cronologico?` |

**Nota:** esta lista corresponde a los mensajes de Claude que se lograron recuperar. No se afirma que sea un registro exhaustivo de todas las interacciones.

## 4. Aprendizaje y comprensión del Valor Ganado (EVM)

El proceso comenzó sin conocimientos previos sólidos sobre EVM. La principal dificultad inicial fue comprender de dónde provenía el AC. Posteriormente se entendió que el **AC (Actual Cost)** representa el costo real incurrido hasta la fecha y se suministra como dato de entrada; no se obtiene a partir del BAC.

Se realizaron ejercicios con escenarios hipotéticos para practicar las fórmulas:

- PV = BAC × porcentaje planificado.
- EV = BAC × porcentaje real completado.
- CV = EV − AC.
- SV = EV − PV.
- CPI = EV / AC.
- SPI = EV / PV.
- EAC = BAC / CPI.
- VAC = BAC − EAC.

También se revisó la interpretación general de los indicadores: CPI por encima de 1 representa un desempeño favorable frente al costo y por debajo de 1 indica un desempeño desfavorable; SPI por encima de 1 indica adelanto frente al plan y por debajo de 1 indica retraso.

Se trabajaron casos especiales, como AC igual a cero o PV igual a cero, en los que el indicador correspondiente no puede determinarse mediante una división convencional. Se consideró más apropiado representar el indicador como no disponible que mostrar un valor engañoso.

Otro aprendizaje fue que los indicadores consolidados del proyecto deben calcularse a partir de los valores agregados de PV, EV y AC, y no mediante el promedio simple de los CPI o SPI de las actividades.

## 5. Decisiones y diferencias frente a las sugerencias de la IA

### 5.1. Tolerancia configurable según el BAC

Durante la revisión de los indicadores se identificó que un valor como CPI = 0.99996 podría mostrarse redondeado como 1.00, aunque todavía exista una pequeña desviación respecto al valor de referencia.

Se propuso manejar niveles de tolerancia relacionados con el BAC, porque una misma desviación porcentual puede representar impactos monetarios diferentes según el tamaño del presupuesto. También se planteó que los umbrales pudieran modificarse posteriormente por personas del negocio o del proyecto.

Los valores inicial de tolerancia y los rangos de BAC utilizados en la implementación se tomaron como una propuesta de referencia discutida con la IA y aceptada para esta versión. No se presentan como umbrales definidos a partir de un estudio estadístico o de una política corporativa.

La tolerancia se utiliza para clasificar el estado de los indicadores; no modifica las fórmulas de EVM. Se aplica según el BAC de la actividad y, para el consolidado, según el BAC total del proyecto.

### 5.2. Otras decisiones

No se identificó una segunda decisión técnica en la que se haya rechazado explícitamente una recomendación concreta de la IA. Durante el proceso sí se redirigieron las conversaciones cuando se alejaban de las prioridades del reto, pero esto se registra como una decisión de gestión del trabajo y no como una segunda decisión de diseño técnico.

## 6. Verificación de los cálculos y de la solución

La comprensión de EVM se validó primero mediante ejercicios manuales con escenarios hipotéticos. Posteriormente, se contrastaron los resultados de la implementación con un caso de prueba conocido:

- BAC: 10.000.000
- Avance planificado: 50 %
- Avance real: 40 %
- AC: 5.000.000
- PV esperado: 5.000.000
- EV esperado: 4.000.000
- CV esperado: -1.000.000
- SV esperado: -1.000.000
- CPI esperado: 0,80
- SPI esperado: 0,80

Los resultados observados en la aplicación coincidieron con estos valores.

También se ejecutó la suite automatizada: **117 pruebas aprobadas** y **100 % de cobertura reportada** con `pytest-cov`. Se verificó el estilo con Ruff y la compilación del frontend con `npm run build`.

La cobertura reportada corresponde a la ejecución de las pruebas sobre el código instrumentado por la herramienta; no debe interpretarse como garantía de ausencia de defectos.

## 7. Decisión de arquitectura

La organización del backend en capas fue propuesta inicialmente por Claude y aceptada durante el desarrollo. Por tanto, no se presenta como una decisión arquitectónica independiente del desarrollador.

La estructura separa responsabilidades entre routers, servicios, dominio y repositorios/base de datos. Esta organización permite mantener las reglas de negocio y los cálculos EVM separados de la capa HTTP y del acceso a datos.



## 8. Reflexión personal

El reto comenzó con un conocimiento limitado de EVM. La principal dificultad fue entender los conceptos y, especialmente, el origen del AC. Los ejercicios con escenarios hipotéticos ayudaron a comprender las fórmulas y a interpretar los indicadores antes de depender de los resultados de la aplicación.

Durante el uso de asistentes de IA fue necesario orientar nuevamente las conversaciones cuando se profundizaba en asuntos que no eran urgentes para completar la entrega. Esto permitió volver a priorizar las pruebas, el funcionamiento de la aplicación, la documentación y la preparación de la sustentación.

Si tuviera que enfrentar nuevamente un reto similar, empezaría por estudiar los conceptos de EVM, definiría con mayor detalle cómo quiero presentar visualmente el frontend y dejaría la preparación de la sustentación como una actividad planificada desde etapas más tempranas.

## 9. Transparencia y alcance del registro

Este documento diferencia entre:

- **Prompts textuales recuperados:** se reproducen tal como fueron conservados.
- **Descripción de consultas a ChatGPT:** se resume el propósito de las consultas porque no se cuenta con una transcripción literal completa.
- **Decisiones propias y propuestas de IA:** se indica cuándo una idea fue propuesta por un asistente y aceptada, en lugar de atribuirla incorrectamente al desarrollador.

El objetivo es documentar de forma honesta cómo se utilizaron las herramientas de IA y cómo se validó la solución.
