# Bitácora mentor (clean-room)

Fuente: extracto de agente ciego, 2026-09-29. **No es la solución.** No hay citas literales de Adrián; el grupo solo dijo “criterio del profesor”.

Uso: checkpoint oral. Notebook cerrado. Si una pregunta se responde con un número del grupo, está mal: medilo en *tu* muestra.

P3 entrega Moodle: **09/10**. Cuerpo de `TP3.md`: no supervisado + supervisado + buscador. Fallos completos: opcionales. Video/jornadas: otra entrega.

No se usa como receta (visto en el extracto y **prohibido decidirlo por ellos**): cómo armaron el target, keep/drop, modelos, métricas reportadas, picos temporales, “el profesor dijo conservar duplicados”.

## Inventario de esquema (tipo D)

Verificar en la muestra oficial, no copiar como verdad del corpus completo.

- **Ids:** `id-infojus`, `guid`, `numero-sumario`, `numero-fallo`, `numero-interno`, `uid-alta`, `uid-mod`, `identificacion-plenario`
- **Texto candidato:** `sumario`, `texto`, `texto-doc`, `texto-completo`, `hechos`, `sintesis`, `caratula`, `titulo`, `titulo_noticia`, `descriptores`, `sobre`, `citas`, `referencias-normativas`, `jurisprudencia-vinculada`, `doctrina-relacionada`
- **Tiempo candidato:** `fecha`, `fecha-alta`, `fecha-mod`, `timestamp`, `timestamp-m`, `timestamp-alta`, `fecha-umod`, `fecha_alta`, `fecha_umod`, `fecha_newsletter`, `fecha_destacada`
- **Otras columnas vistas:** `numero-sumario`, `materia`, `sumario`, `descriptores`, `referencias-normativas`, `texto`, `fuente`, `analista`, `responsable`, `fecha`, `tipo-tribunal`, `instancia`, `jurisdiccion`, `provincia`, `caratula`, `fecha-alta`, `fecha-mod`, `uid-alta`, `uid-mod`, `timestamp`, `timestamp-m`, `timestamp-alta`, `id-infojus`, `fecha-umod`, `titulo`, `guid`, `numero-fallo`, `tribunal`, `pais`, `tipo-fallo`, `localidad`, `magistrados`, `actor`, `demandado`, `sobre`, `sumarios-relacionados`, `texto-doc`, `sala`, `numero-interno`, `tribunal-origen`, `publicacion`, `texto-completo`, `numero-camara`, `citas`, `jurisprudencia-vinculada`, `sintesis`, `hechos`, `identificacion-plenario`, `doctrina-relacionada`, `referencias-juris`, `control-constitucional`, `disidencia`, `esq-clasificacion`, `seq`, `archivo`, `tipo-norma`, `org_emisor`, `fecha_alta`, `ppublic_nov`, `d_link`, `fecha_umod`, `status`, `titulo_noticia`, `destacada`, `fecha_newsletter`, `suplemento_bo`, `subtipo`, `url_portal`, `nro_orden`, `fecha_destacada`, `sigla_emisor`
- Anidadas: `descriptores`, `jurisdiccion`, `referencias-normativas`
- Auxiliar: HF `marianbasti/jurisprudencia-Argentina-SAIJ`; muestra `datos/`; opcional `datos/fallos/`

## Cuestionario

### Datos y unidad de análisis

- ¿Cada fila es un fallo, un sumario, una novedad editorial u otra cosa, y cómo se distingue?
- ¿El mismo caso judicial puede aparecer más de una vez con ids o textos distintos?
- ¿Qué prefijos o convenciones tiene `id-infojus` y qué implica un id nulo?
- ¿`guid` identifica lo mismo que `id-infojus`?
- Verificá cobertura cruzada: qué campos existen en un tipo de registro y faltan en otro.
- ¿`tribunal` y `tipo-tribunal` miden la misma cosa?
- ¿`jurisdiccion`, `provincia`, `localidad` y `pais` son consistentes entre sí?
- ¿Las columnas de esquema noticia/norma pertenecen a la unidad de jurisprudencia?
- ¿Hay estructura anidada que hay que aplanar antes de contar nulos o vocabularios?
- ¿Trabajás con la muestra de `datos/` o con el corpus completo, y cómo lo documentás?
- ¿Los PDF/TXT de `datos/fallos` se alinean 1:1 con filas del JSONL?
- Verificá duplicados exactos vs mismo texto con metadatos distintos vs mismo id.
- ¿Qué hacés si el texto está vacío pero hay sumario/carátula, o al revés?

### Target y leakage

- ¿Cuál es la variable objetivo y de qué campo sale?
- ¿El target ya viene colapsado o hay que construirlo? ¿Una etiqueta, combinaciones, multi-etiqueta?
- ¿`materia` puede listar más de un valor en la misma fila?
- ¿Usar `materia`, descriptores, tribunal, jurisdicción o provincia como feature es leakage si el target es fuero/rama?
- ¿El README (“predecir leyendo exclusivamente el sumario”) choca con usar metadatos institucionales?
- ¿Hay el mismo texto con etiquetas distintas?
- ¿`analista` / `responsable` / `fuente` explican la etiqueta más que el texto?
- Verificá si `sumarios-relacionados` o ids cruzados filtran el target al test.
- ¿Plantillas en descriptores contaminan texto o etiqueta?

### Sesgo / desbalance / tiempo

- ¿Hay desbalance entre fueros/materias y entre tribunales?
- ¿Qué reloj temporal usarías para actividad judicial vs carga al sistema?
- ¿Un pico o un hueco es fenómeno jurídico o artefacto de digitalización?
- ¿Hay sesgo geográfico o de instancia que un modelo puede memorizar?
- ¿Las clases raras son errores, categorías reales o compuestos?
- ¿El desbalance invalida accuracy como métrica principal?
- ¿Un split aleatorio mezcla épocas y filtra el futuro?
- ¿Hay fechas imposibles o tipos mezclados?

### Texto y representación

- ¿Qué campo de texto es el adecuado para cada TP y por qué no concatenar a ciegas?
- ¿`sumario` y `texto` son el mismo contenido con otro nombre?
- ¿Markup, citas `[[…]]` o ruido OCR cambian longitud y vocabulario?
- ¿Las stopwords jurídicas se comportan como las genéricas?
- ¿Lematizar/normalizar pierde locuciones legales?
- ¿Longitud y vocabulario bastan para elegir campo?
- ¿BoW, TF-IDF y embeddings contestan preguntas distintas acá?
- Si hay embeddings: ¿input natural o ya lematizado?
- ¿Los n-gramas legales se rompen al tokenizar?
- Fallos completos: ¿los procesás y cómo contrastás ruido vs sumarios?

### Split y métricas

- ¿La unidad de split es la fila, el texto único, el id de caso o el tiempo?
- ¿Un mismo texto en train y test es fuga aunque el id sea distinto?
- ¿Hace falta estratificar? ¿Por clase simple o por combinación?
- ¿Ajustar el vectorizador con todo el corpus (incluido test) es fuga?
- ¿Multiclase vs multi-etiqueta y qué métricas deja inválidas?
- ¿Accuracy, F1 micro/macro, Hamming y subset accuracy miden cosas distintas acá?
- ¿Hiperparámetros solo con CV en train y test una vez?
- ¿Cómo evaluás clases chicas sin que las grandes dominen?

### No supervisado

- ¿Los grupos latentes se recuperan sin usar el target como input?
- ¿Cómo medís correspondencia con categorías legales sin convertir clustering en clasificación disfrazada?
- ¿Qué criterio usás para comparar representaciones en temas latentes?
- ¿Ajustar TF-IDF/SVD en todo el corpus es aceptable en no supervisado y prohibido al pasar a supervisado?
- Verificá documentos con vector nulo.

### Búsqueda semántica

- ¿La consulta es lenguaje natural y la colección son embeddings de qué campo?
- ¿Cómo cambia la recuperación con jerga técnica vs hechos en coloquial?
- ¿Con qué definís “relevante” si no hay qrels?
- ¿Un match léxico puede parecer semántico y no serlo?
- ¿El buscador puede devolverte el documento de la propia consulta por id duplicado?
- ¿El DISCLAIMER impide presentarlo como herramienta jurídica?

### Entrega

- ¿TP1 es reporte visual, no un modelo?
- ¿TP2 justifica altas/bajas de variables, no solo un dataframe?
- ¿TP3 son las tres patas del `TP3.md` o el aula “o ambos”? (Sprint: las tres.)
- ¿Los fallos completos sustituyen el JSONL? (No.)
- ¿Hay que citar Apache 2.0 y el aviso de no-asesoramiento?

## Incertidumbre del extracto

- Sin rúbrica oficial ni prohibición explícita de accuracy en los TP.md
- PDF del grupo ilegible; TP2 del grupo serializado en una línea
- El TP3 del grupo no llega al buscador: no implica que nosotros lo saltemos
- Esquema live de HuggingFace y PDFs de `datos/fallos` no verificados
