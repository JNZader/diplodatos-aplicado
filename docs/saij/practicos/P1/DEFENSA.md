# P1 — Defensa (consigna → respuesta → por qué)

Esto **no** es la entrega. Es para que puedas explicar el práctico.

- **Lab:** `p1_eda.ipynb` (código, se re-corre).
- **Defensa (este archivo):** cada ítem de la consigna, qué respondimos, por qué, qué no prueba.
- **Entrega:** informe imprimible. Todavía no: falta el bloque de texto (D2).

**Datos:** muestra oficial `dataset_sample.jsonl.gz` (8.748 filas). No es el SAIJ completo. Las cifras de acá valen para **esta muestra**.

**Pendiente D2:** exploración de textos, stopwords, n-gramas, reporte visual de cierre.

---

## Cómo leer esto

Cada sección tiene:

1. **Consigna** — lo que pide el mentor.
2. **Respuesta** — en 5–10 líneas, lo que dirías en un oral.
3. **Por qué** — evidencia nuestra (números de la muestra).
4. **No prueba** — el error típico si exagerás.

---

## 1. ¿Qué información hay? ¿Qué se puede preguntar?

**Consigna.** Entender el corpus: qué hay y qué preguntas se pueden responder.

**Respuesta.** El JSONL mezcla **más de un tipo de registro** en las mismas 71 columnas. Hay sumarios (prefijo `SU`), fallos (`FA`) y tres novedades (`NV`). También hay ~1.000 filas vacías de plantilla. Se puede preguntar por fueros, tribunales, geografía y tiempo, **pero no sobre una única unidad “fallo”** sin filtrar.

**Por qué.** 8.748 filas. 1.035 son plantilla (sin `id-infojus`, sin `materia`, descriptores dummy). Quedan 7.713. `guid` es único pero está **todo** anonimizado (`123456789-…`): no sirve para decir “un caso = un guid”. Prefijos: SU 4.851, FA 2.859, NV 3.

**No prueba.** Que el corpus completo de HuggingFace tenga la misma mezcla. Es una muestra.

---

## 2. Distribución de fueros y tribunales

**Consigna.** Evaluar distribución de fueros y tribunales.

**Respuesta.** No hay una columna que se llame `fuero`. Lo más parecido es `materia`, y **solo existe en los SU**. Los FA no tienen materia. Tribunales: `tipo-tribunal` son códigos (`CS`, `CC`, `LB`…) — 139 valores — no un fuero limpio.

**Por qué.** `materia` no nula: 4.851 (62,9 % de las filas de trabajo). 282 valores distintos. Top: PROCESAL 684, PENAL 527, LABORAL 483, CIVIL 459, CIVIL - COMERCIAL 419. `tipo-tribunal` top: CS 2.877, CC 1.048, LB 565, PN 555.

**No prueba.** Que PROCESAL sea un fuero. Es una etiqueta de `materia`. Que CS sea “Corte Suprema” hasta que documentemos el código.

---

## 3. Valores faltantes

**Consigna.** Indagar si hay valores faltantes.

**Respuesta.** Sí, y no son “un poco de NA”. Hay columnas **siempre vacías** en la muestra (`doctrina-relacionada`, `disidencia`, …), campos anidados (`descriptores`, `jurisdiccion`) que no se cuentan como un string, y faltantes **estructurales**: un FA no “olvidó” el sumario — ese tipo de fila no lo trae.

**Por qué.** Mediana 23 campos no nulos de 71. Cobertura: SU tiene materia/sumario ≈ 100 % y tribunal 0 %. FA tiene tribunal 100 % y materia/sumario 0 %. Eso no es MCAR.

**No prueba.** Que haya que imputar `materia` en los FA. Imputar mezclaría unidades.

---

## 4. Desbalance de clases

**Consigna.** ¿Hay desbalance?

**Respuesta.** Sí, si tomás `materia` como clase: PROCESAL y PENAL pesan mucho; hay colas de 20–30 filas. Además CABA+PBA dominan provincia. Accuracy en un modelo futuro mentiría.

**Por qué.** Top 5 de `materia` ya se comen una fracción grande de los 4.851 SU. Provincia: CABA 3.591, Buenos Aires 1.337, después un salto.

**No prueba.** Las proporciones exactas del corpus completo. Ni cuál es *la* clase del modelo: todavía no hay target cerrado.

---

## 5. Evolución temporal y sesgo temporal

**Consigna.** Evolución temporal; sesgos temporales.

**Respuesta.** Hay **varios relojes**. `fecha` parece del documento (a veces *varias* fechas en un string, separadas por `|`). `timestamp` está en milisegundos y se parece a **carga al sistema** (arranca ~2012). Solo el 12 % de las filas con ambos relojes coinciden en el año. Un pico de timestamp no es “ese año se emitieron más fallos”.

**Por qué.** 166 `fecha` con `|`. `fecha` parseada ~1865–2026. Timestamp plausible ~2012–2026 UTC. 6.606 filas con ambos; mismo año 12,4 %; el documento es anterior al timestamp en esas 6.606.

**No prueba.** Migración, digitalización ni “boom de 1996”. Eso sería interpretar el pico de `fecha` sin el otro reloj.

---

## 6. Áreas más/menos representadas

**Consigna.** Qué áreas legales están más o menos representadas.

**Respuesta.** En `materia` (solo SU): más PROCESAL / PENAL / LABORAL / CIVIL. Menos: colas (tributario, contravencional, combos raros). Geografía: CABA y PBA. Córdoba es chica en *esta* muestra.

**Por qué.** Ver top 20 de `materia` y top de `provincia` en el notebook.

**No prueba.** Que el derecho argentino “sea” eso. Es sesgo del recorte SAIJ + de la muestra.

---

## 7. Tribunales sobrerrepresentados

**Consigna.** ¿Hay tribunales sobrerrepresentados?

**Respuesta.** Sí: el código `CS` aparece ~2.877 veces, lejos de `CC` (~1.048). Hay 139 códigos; la cola es larga. `instancia` está sucia (`S S S S` repetido).

**Por qué.** Value counts de `tipo-tribunal` e `instancia`.

**No prueba.** Que debamos tirar los tribunales chicos. En TP2 se decide. En TP3, usar tribunal como feature puede ser **leakage** si el target es fuero.

---

## 8. Identificar la variable objetivo (target)

**Consigna.** Identificar el target que vamos a predecir.

**Respuesta (aún no cerrado).** El proyecto (README) pide predecir el **fuero / rama** leyendo el **sumario**. El campo más cercano es `materia`, pero:

- no está en los FA;
- mezcla fuero (`PENAL`) con tipo de acto (`PROCESAL`);
- hay combos (`CIVIL - COMERCIAL` vs `CIVIL-COMERCIAL`);
- 891 materias de la muestra no tienen ni un token típico de fuero.

Hoy: **candidato = fuero a partir de `materia` en filas SU**, receta de colapso **no escrita**. Congelarlo ahora sería inventar la etiqueta.

**Por qué.** Tokenización grosera sobre `materia`: muchos CIVIL+COMERCIAL juntos; un montón sin token de fuero.

**No prueba.** La receta del grupo (cómo agrupar, “OTROS”, multi-hot). Eso está en cuarentena.

**Leakage (para no olvidar).** Si el target nace de `materia`, no podés usar `materia` ni descriptores que la parafrasean como feature, si el juego es “solo el sumario”.

---

## 9. Textos (pendiente D2)

**Consigna.** Elegir campo de texto; longitudes; vocabulario; frecuentes; n-gramas; distintivos vs compartidos por fuero; stopwords. Opcional: fallos completos.

**Respuesta hoy.** Campo candidato: `sumario` en filas SU (ahí hay texto). `texto` a menudo convive con `sumario` — hay que ver si son el mismo contenido. FA no traen esos campos. Fallos completos: **no** en este sprint salvo que sobre tiempo.

**Por qué.** Cobertura SU vs FA (sección 1).

**No prueba.** Nada de léxico todavía: no se corrió.

---

## 10. Reporte visual (pendiente D2)

**Consigna.** Armar un reporte visual con hallazgos preliminares.

**Respuesta hoy.** Hay dos pares de barras (materia / provincia y los dos relojes). No es el informe de cierre.

---

## Oral (sin notebook)

1. ¿Por qué una fila no es siempre un fallo?  
2. ¿Por qué no congelarías `materia` cruda como fuero?  
3. Si hay que predecir fuero *desde el sumario*, ¿qué metadato sería leakage?  
4. ¿Qué reloj usarías para actividad judicial y cuál no?

Si no sale, leé **solo** las secciones 1, 5 y 8.
