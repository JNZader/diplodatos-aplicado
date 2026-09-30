# Sprint SAIJ — P1 + P2 + P3 (29/09 → 09/10/2026)

Objetivo: **entregar y poder defender** los tres prácticos. No es “toda la diplomatura”.
G01 y cualquier doc de compañeros: **cuarentena**. No se pegan acá ni se abren mientras se escribe ese TP.

Fuente oficial del mentor (repo, last push **2026-07-08**):
https://github.com/adrian-alejandro/mentoria-diplodatos-2026-clasificacion-y-busqueda-textos-legales

- `prácticos/TP1.md` entrega **07/08** — coincide con lo que pegaste.
- `prácticos/TP2.md` entrega **04/09** — tu primer pegado decía 28/08. El repo manda hasta que Moodle diga otra cosa.
- `prácticos/TP3.md` entrega **02/10** en el repo (julio). Moodle/coordinación = **09/10** (confirmado 29/09). Sprint anclado a **09/10**.
- El cuerpo de TP3.md pide **los tres**: no supervisado + supervisado + **motor de búsqueda semántica**. El título dice “o ambos”; el texto no. Para “mejor resultado” el buscador **no es extra**.
- D1 no baja 2.5 GB: hay `datos/dataset_sample.jsonl.gz` (~5.7 MB) + notebook de descarga. Fallos completos = opcional (`datos/fallos/`).

Ventana (si vale 09/10): **11 días**. P1 y P2 vencidos: producirlos igual. Si Moodle dice P3 = **02/10**, este plan de 11 días muere y se pasa a recorte de pánico (solo supervisado + TF-IDF, sin buscador).

## Reglas (no negociables)

1. Cada día cierra con **checkpoint oral**: 5 minutos, notebook cerrado, responder las preguntas del día. Si no podés, el día no está hecho.
2. **Muestra primero.** Iterar en 80k–100k estratificado por fuero. El JSONL completo (~2.47 GB, 874.845 filas) entra recién para validar P2 y entrenar P3.
3. Un artefacto por práctico: notebook + narrativa (markdown en el mismo notebook alcanza). Carpeta: `practicos/P1/`, `practicos/P2/`, `practicos/P3/`.
4. Prohibido: guía de 85k como lectura, Ética, RAG productivo, fallos completos opcionales, 6 modelos, lematizar “como el paper”.
5. Techo diario **12 h de laburo real**. **15 h = solo** si un entrenamiento se rompe o Moodle se pone pesado. Dormir ≥ 6.5 h. Sin eso no hay “entender”.
6. Si a las 22:30 no hay output del día, **cortá alcance**, no alargues teoría.
7. **Clean room por TP** (ver abajo). Contrastar con el grupo **después** de congelar ese práctico, nunca durante.

## Clean room

Esto **no** es un clean room legal de IP. Es un protocolo para que el entregable sea tuyo y lo puedas defender.

**Entrada permitida (sala limpia)**
- `prácticos/TP1.md` / `TP2.md` / `TP3.md` del repo del mentor
- `datos/dataset_sample.jsonl.gz` + notebook de descarga
- DISCLAIMER / README de datos
- tu notebook del día y el checkpoint oral

**Cuarentena (no abrir, no pegar, no adjuntar al chat)**
- `Mentoria_trabajo_G01.ipynb` / PDF
- slides, informes o notebooks de compañeros
- la guía SAIJ de 85k como receta de este TP

**Contraste (sala sucia, acotada)**
Después de **congelar** ese práctico: 30–45 min. Solo diferencias de hallazgo (órdenes de magnitud, target, leakage). Si el grupo hizo algo que vos no, o lo redescubrís con tu evidencia o lo dejás documentado como “no lo vi”. No se copia código ni narrativa.

**Contaminación ya existente en esta sesión (no se puede borrar)**
G01 ya fue inspeccionado en agosto: ~874k filas, sample 50%, target desde `materia`, EDA de fueros/texto/TF-IDF. Yo no voy a reabrir ese notebook. Si un número “aparece de memoria”, se trata como **hipótesis** y se mide de nuevo en tu muestra. Si querés un clean room más duro, P2/P3 se pueden hacer en un chat nuevo que no haya visto G01.

### Recuperar al mentor sin copiar al grupo

Son dos cosas distintas. El notebook de tus compañeros **mezcla** avisos de Adrián con *su* solución. Si lo leés, no sabés cuál es cuál.

**Tipo M — mentor (sí)**  
Qué se va a fijar, trampas del dataset, qué es opcional, cómo entregar, preguntas del README. Sin números de resultado ni recetas de código.

**Tipo S — solución del grupo (no, hasta el freeze)**  
Cómo armaron el target, qué columnas tiraron, qué modelo, qué plots, qué concluyeron.

**Cómo sacarlo (en este orden)**
1. Las 10 preguntas del README del repo **ya son** el temario del mentor. Se usan como checklist oral, no como respuestas.
2. Llamada de 15 min a un compañero: “qué dijo Adrián / qué va a mirar”. Prohibido “cómo lo hicieron”. Anotá vos en `practicos/bitacora-mentor.md`.
3. Moodle: anuncios, foro, rúbrica. Eso es mentor, no grupo.
4. Opcional, **otro chat** (no este): un extractor lee G01 una vez y sale **solo** un cuestionario sin respuestas (“¿hay más de un reloj de fecha?”, “¿el target puede filtrarse por descriptores?”). Si una viñeta ya afirma el hallazgo, se tira. Este chat no recibe G01 ni el notebook.
5. Contraste post-freeze: 30–45 min, diferencias, no copy-paste.

No se recupera “haber estado en la clase” leyendo sklearn ajeno. Se recuperan *gotchas*. El entendimiento lo ponés vos con tu muestra.

## Carga total

| | Horas |
|---|---|
| Planificado | **118 h** en 11 días (~10.7 h/día) |
| Pico | D4, D6, D7, D8 → 12 h |
| Reserva | +3 h (hasta 15 h) **solo** D4 o D7–D8 si el bake-off o el fit se cae |
| Fuera de alcance | video 07/11, jornadas 04–05/12 |

Plantilla de día (ajustá el reloj, no las horas):

- 09:00–13:00 bloque A (4 h)
- 13:00–13:45 comida
- 13:45–18:15 bloque B (4.5 h)
- 18:15–19:15 cena / caminar
- 19:15–22:45 bloque C (3.5 h) → en días 10 h, C dura 1.5 h (hasta 21:00)
- 22:45–23:00 checkpoint oral

---

## D1 — mar 29/09 — 10 h — Entorno + P1 estructurado

**Output:** `practicos/P1/p1_eda.ipynb` con secciones 1–estructurado empezadas; `data/sample_100k.parquet`; README de una página con hipótesis del target.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Moodle: ¿P3 es 02/10 o 09/10? ¿P1/P2 aceptan entrega? Entorno. Clonar o copiar del repo del mentor **solo** `datos/dataset_sample.jsonl.gz` + `descarga-lectura-dataset.ipynb`. Leer la muestra con código propio. No hace falta el JSONL de 2.5 GB hoy. |
| B | 4 | Si la muestra es chica, anotar n y sesgo vs corpus completo. Esquema, tipos, nulos, IDs, duplicados. Construir **candidato a target `fuero`**. Conteos, desbalance, top tribunales, provincias. El 100k estratificado entra cuando haga falta más señal, no en D1. |
| C | 2 | Serie temporal: **dos relojes** (fecha del documento vs alta/timestamp). No interpretar picos todavía. Escribir 8–10 oraciones de hallazgos. |

**Checkpoint:** ¿Cuál es la unidad de análisis? ¿Qué predice el target? ¿Por qué no usar timestamp como fecha judicial? ¿Hay fuga obvia (provincia, año, descriptor)?

**No hacer:** plots lindos, texto NLP, leer G01 entero.

---

## D2 — mié 30/09 — 11 h — P1 texto + reporte visual. CONGELAR P1

**Output:** P1 cerrado: estructurado + texto + 8–12 figuras con título que afirma algo. Lista de riesgos para P2.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Elegir **un** campo de texto (sumario vs otros). Longitud, nulos de texto, vocabulario crudo, top unigrams. |
| B | 4.5 | Stopwords on/off. N-gramas. Términos **distintivos por fuero** (no solo frecuentes). Tabla CIVIL vs COMERCIAL (confusión futura). |
| C | 2.5 | Reporte visual: cada figura = pregunta + hallazgo + “esto NO prueba X”. Congelar P1. Copiar riesgos a `practicos/P2/riesgos-desde-p1.md`. |

**Checkpoint:** ¿Qué campo de texto y por qué? ¿Qué palabras son distintivas vs compartidas? ¿Qué sesgo temporal/geográfico va a romper un modelo ingenuo?

**No hacer:** vectorizar, lematizar, sklearn.

---

## D3 — jue 01/10 — 11 h — P2 calidad y recorte

**Output:** reglas de limpieza documentadas; dataset curado de la muestra; tabla keep/drop de columnas.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Nulos: MCAR/MAR/MNAR **en este corpus** (al menos un argumento por columna crítica). Duplicados de ID. Categorías inconsistentes (`materia`, `tipo-tribunal`). Longitudes de texto absurdas. |
| B | 4.5 | Keep/drop con motivo. Variables derivadas (año judicial, log-longitud, flags de fuero). **Prohibir** features que filan el target (descriptores que *son* el fuero, materia cruda si el target sale de ahí). |
| C | 2.5 | Partición **ahora**: train/test (y si hay tiempo, valid) **temporal o estratificada**. Justificar. Aplicar limpiezas **solo con estadísticas de train**. |

**Checkpoint:** ¿Qué columna tiraste que alguien iba a usar mal? ¿Dónde está el leakage? ¿El split respeta tiempo o solo el random de sklearn?

---

## D4 — vie 02/10 — 12 h — P2 texto + representaciones (PICO)

**Output:** bake-off BoW vs TF-IDF vs embeddings en la muestra; **una** ganadora con evidencia.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Normalización mínima (minúsculas, espacios, ruido). Stopwords. Lematización **solo si** un A/B de 90 min muestra ganancia; si no, se documenta “no vale el costo” y se sigue. |
| B | 4.5 | BoW, TF-IDF (1–2 grams, min_df). Embeddings: un modelo liviano (no bajar 4 variantes). Métrica de comparación **antes de P3**: p.ej. kNN/Naive Bayes rápido o silhouette en 5k docs — lo mismo para las tres. |
| C | 3.5 | Elegir representación. Escribir desventajas de las otras dos **en este dataset**. Reserva 15 h acá si el embedder no corre. |

**Checkpoint:** ¿Por qué ganó esa representación **acá**, no en el tutorial? ¿Qué se pierde (rareza de fueros, n-gramas jurídicos, costo)?

---

## D5 — sáb 03/10 — 10 h — Validar P2 en más datos. CONGELAR P2

**Output:** P2 cerrado. Parquet/train-test listos para P3. Nota de “qué cambiaría con 874k”.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Repetir limpiezas + TF-IDF/embeddings en muestra más grande o 50% si la RAM aguanta. Contrastar 3 números contra G01 (no el notebook: los **hallazgos**). Si divergís, gana tu evidencia o explicás el sesgo de muestra. |
| B | 4 | Empaquetar P2: pipeline reproducible (script o celdas ordenadas). Seed, versiones, rutas. |
| C | 2 | Narrativa P2. Congelar. |

**Checkpoint:** ¿Alguien puede re-correr P2 de cero? ¿El test set sigue intacto?

---

## D6 — dom 04/10 — 12 h — P3 no supervisado

**Output:** clustering/temas latentes; comparación con fueros; qué representación agrupa mejor.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | k-means o NMF/LDA **uno**. k por criterio (elbow/silueta **y** sentido jurídico). |
| B | 4.5 | Términos por cluster vs etiquetas de fuero (ARI/NMI o tabla cruzada). Hallazgo: “el cluster no es el fuero” o sí, con evidencia. |
| C | 3.5 | Figuras + límites (k arbitrario, sample bias). |

**Checkpoint:** ¿Los temas latentes coinciden con categorías legales o con otra cosa (provincia, década, tipo documental)?

---

## D7 — lun 05/10 — 12 h — P3 supervisado (eje principal)

**Output:** Dummy + 1 modelo serio; métricas por clase; split honesto.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Tipo de problema (multiclase, desbalance). Métricas: **no** accuracy. Macro-F1 + por clase (CIVIL/COMERCIAL obligatorias). Dummy stratified. |
| B | 4.5 | Un modelo (NB o Linear SVM o LR). Misma representación ganadora de P2. Comparar contra BoW barato si hay tiempo (2 h max). |
| C | 3.5 | Matriz de confusión, errores sistemáticos. Reserva 15 h si el fit explota. |

**Checkpoint:** ¿Qué clase pierde y por qué? ¿El modelo usa leakage? ¿Baseline vs modelo: cuánta ganancia real?

---

## D8 — mar 06/10 — 12 h — Errores + el otro eje cerrado

**Output:** análisis de errores; si D6 o D7 quedó flaco, se termina. No se empieza un tercer modelo.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Muestrear 20 errores a mano. Hipótesis (sumario corto, fuero mixto, materia sucia). |
| B | 4.5 | Cerrar el eje más débil (cluster o clasificador). |
| C | 3.5 | Sección “limitaciones” de P3. |

**Checkpoint:** ¿Podés explicar 3 errores sin decir “el modelo falló”?

---

## D9 — mié 07/10 — 10 h — Buscador (está en TP3.md del repo)

El cuerpo oficial pide: query en lenguaje natural → fallos relevantes con embeddings. El mail de coordinación no lo nombra; el `prácticos/TP3.md` sí. En este sprint **entra**. Si D7–D8 no están defendibles, se recorta acá y se documenta la deuda.

**Output:** query → top-k fallos con embedding de P2. 5 queries jurídicas reales. No UI.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Índice (numpy/faiss si ya está; si no, brute force en 20–50k). |
| B | 4 | 5 queries, inspección cualitativa, 1 fallo conocido vs basura. |
| C | 2 | Párrafo: esto **no** es RAG. |

Si D7–D8 no están defendibles: **cancelá D9 buscador** y usá las 10 h para P3. El 09/10 se aprueba el práctico, no el producto.

---

## D10 — jue 08/10 — 10 h — Empaquetar los tres

**Output:** tres notebooks corridos de punta a punta en muestra; READMEs; PDF o HTML export si Moodle lo pide.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Releer P1/P2 como mentor hijo de puta: claims vs figuras. Borrar celdas muertas. |
| B | 4 | P3: métricas finales, semillas, “cómo reproducir”. |
| C | 2 | Subir P1 y P2 a Moodle si el buzón vive. |

**Checkpoint:** ¿Cada práctico tiene objetivo, método, hallazgo, límite, siguiente paso?

---

## D11 — vie 09/10 — 8 h — Entrega P3

**Output:** P3 en el buzón. Copia local. No features nuevas después de las 15:00.

| Bloque | Horas | Qué |
|---|---|---|
| A | 4 | Corrida final, capturas, checklist Moodle. |
| B | 3 | Video no. Informe corto si piden. |
| C | 1 | Apagar. Lista de deudas para el video del 07/11. |

---

## Orden de pánico (si te atrasás)

1. Sacrificá buscador (D9).
2. Sacrificá lematización y embeddings pesados: TF-IDF + Linear SVM.
3. Sacrificá “ambos” de P3: **quedate con supervisado** (el target nace en P1).
4. Nunca sacrifiques split honesto, métricas por clase, ni la narrativa.

## Material que sí se usa

- Consignas que pegaste (P1 07/08, P2 28/08, P3 09/10).
- G01 como lista de preguntas y órdenes de magnitud para contrastar.
- Dataset HF. No está en el repo todavía: D1 lo baja.

## Explicitamente no es este sprint

Video 07/11, jornadas diciembre, guía SAIJ de 85k, curso de Ética, repo del mentor como dependencia de la entrega, 874k en D1.
