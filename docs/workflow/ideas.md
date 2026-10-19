---
title: Resumen - App notas manuscritas a Obsidian
tags: [proyecto, obsidian, telegram, ocr, pipeline]
fecha: 2026-10-18
---

# App: notas manuscritas → Obsidian

**Objetivo:** tomar una foto de apuntes (o un PDF de GoodNotes), extraer el texto, ponerle título y tags, y guardarlo como Markdown en Obsidian, con ecuaciones en LaTeX y esquemas en Mermaid.

**Idea clave:** el costo de la API es casi despreciable (centavos al mes). El costo real es tiempo de desarrollo y mantención, así que conviene optimizar por simplicidad.

---

## 1. Pipeline

```
Captura (Telegram: foto / documento / PDF)
   ↓
Ingesta: descargar + registrar en BD (hash, estado)
   ↓
Preproceso: PDF → imágenes, resize, rotación
   ↓
Extracción: modelo de visión → JSON estructurado
   ↓
Validación: esquema JSON + LaTeX compila + reintento
   ↓
Render: JSON → Markdown con frontmatter
   ↓
Escritura: .md + imágenes en el vault
   ↓
Respuesta por Telegram (título, costo, errores)
```

s libres, recortar y embeber la imagen).

---

## 2. Elección del OCR

| Opción | Calidad (manuscrito + ecuaciones) | Costo aprox./página | Comentario |
|---|---|---|---|
| LLM con visión (Claude, Gemini Flash, GPT mini) | Muy buena | ~$0.001-0.01 | OCR, título, tags y LaTeX en una llamada |
| Mathpix | Excelente en ecuaciones | ~$0.002-0.01 | No titula ni clasifica |
| Local (olmOCR, Surya, pix2tex, Qwen-VL) | Media en manuscrito | $0 + hardware | Más mantención |
| Tesseract | Mala en manuscrito | $0 | Descartado |

**Recomendación:** modelo de visión económico (tipo Haiku o Flash) y escalar a uno mejor solo si falla. Las cifras son órdenes de magnitud: verificar precios vigentes.

**Cuenta rápida:** ~1.500 tokens de entrada + ~700 de salida por página → ~$0.002-0.006. 300 páginas al mes ≈ $1-2.

---

## 3. Organization and contracts

notes2obsidian/
├── pyproject.toml
├── uv.lock
├── README.md
├── main.py                      # punto de entrada, muy corto
├── src/
│   └── notes2obsidian/
│       ├── __init__.py          # marca la carpeta como paquete
│       ├── config.py            # lee .env y ajustes
│       ├── models.py            # modelos Pydantic (Nota, ResultadoOCR)
│       ├── preprocess.py        # PDF → imágenes, resize
│       ├── extractor.py         # llamada al LLM de visión
│       ├── validate.py          # chequeo de LaTeX y esquema
│       ├── render.py            # JSON → Markdown
│       ├── storage.py           # SQLite, hashes, escritura al vault
│       ├── pipeline.py          # une los pasos anteriores
│       └── bot.py               # handlers de Telegram
└── tests/
    ├── test_render.py
    └── test_preprocess.py

**models.py** : contract, how the data flows in the app \
**pipeline.py** : how the different scripts are communicated
**bot.py** : Telegram API configuration
**render.py** : from files (PDFs, PNGs, etc) to markdown