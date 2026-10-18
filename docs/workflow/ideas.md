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

**Salida estructurada del modelo:** `titulo`, `tags`, `resumen`, `cuerpo_markdown`.

- Ecuaciones: `$...$` y `$$...$$` (Obsidian las renderiza con MathJax).
- Esquemas: bloques ```` ```mermaid ```` (solo sirve para grafos y flujos; para dibujos libres, recortar y embeber la imagen).

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

## 3. Optimización de costos

1. Reducir imágenes (lado largo ~1.500-2.000 px).
2. Batch API (~50% de descuento en varios proveedores) para procesamiento nocturno.
3. Prompt caching del system prompt y el esquema JSON.
4. Hash de contenido para no reprocesar.
5. PDFs de GoodNotes con texto seleccionable: extraer con PyMuPDF y usar el LLM solo para título y limpieza.
6. Cascada de modelos: barato primero, mejor solo si falla.
7. Una llamada por página con salida JSON.
8. Límite de gasto mensual en la cuenta del proveedor.

---

## 4. Ejecución en Mac

- Un proceso en espera (long polling de Telegram) consume ~0% CPU y ~30-60 MB de RAM. El trabajo pesado ocurre en la API.
- **LaunchAgent** en `~/Library/LaunchAgents/com.renato.notas2obsidian.plist` con `RunAtLoad` y `KeepAlive`.
- Cargar con `launchctl load <plist>` (o `launchctl bootstrap gui/$(id -u) <plist>`).

**Cuidados:**
- Usar la ruta absoluta del Python del venv.
- launchd no lee `.zshrc`: guardar la API key en `.env` o Keychain.
- Permisos de macOS (Acceso total al disco) si se vigilan carpetas de iCloud.
- Escaneo inicial al arrancar para procesar lo que llegó con el Mac apagado.
- Reintentos con espera si aún no hay red.

---

## 5. Stack y opciones por paso

| Paso | Opción recomendada | Alternativas |
|---|---|---|
| Lenguaje / entorno | Python 3.12 + uv | venv + pip |
| Calidad | ruff + pytest | mypy |
| Config | pydantic-settings + .env | python-dotenv, Keychain |
| Captura | python-telegram-bot | aiogram |
| Estado | SQLite (`sqlite3`) | SQLModel / SQLAlchemy, JSON simple |
| Hash | `hashlib.sha256` | - |
| PDF → imagen | PyMuPDF | pdf2image (requiere poppler) |
| Imágenes | Pillow | OpenCV (deskew, recorte de figuras) |
| Extracción | API LLM con visión + Pydantic | Mathpix, modelos locales |
| Reintentos | tenacity | - |
| Validación LaTeX | katex (Node) | latex2mathml |
| Validación Mermaid | mermaid-cli (opcional) | - |
| Render | Jinja2 / f-strings | - |
| Frontmatter | python-frontmatter | YAML a mano |
| Operación | launchd + logging | structlog, Docker |

**Escritura segura:** archivo temporal + `os.replace`, título sanitizado y manejo de colisiones.

---

## 6. Roadmap

- [ ] **Fase 0, preparación:** repo git, `uv init`, ruff, pytest, bot en BotFather, API key con límite de gasto.
- [ ] **Fase 1, núcleo sin Telegram:** `python run.py foto.jpg` → `.md`. Probar con 10-20 páginas reales para elegir modelo.
- [ ] **Fase 2, robustez:** esquema Pydantic, plantilla Markdown, PDF multipágina, tests.
- [ ] **Fase 3, estado:** SQLite con hashes y estados; idempotencia.
- [ ] **Fase 4, Telegram:** handlers para foto, documento y PDF (enviar como archivo para evitar compresión).
- [ ] **Fase 5, automatización:** LaunchAgent, escaneo inicial, reintentos, logs rotados.
- [ ] **Fase 6, calidad:** validación de LaTeX, cascada de modelos, tabla de costos, comando `/costos`.
- [ ] **Fase 7, extras:** recorte de figuras, Mermaid, enlaces entre notas, prompt caching y batch.
- [ ] **Fase 8, multiusuario (futuro):** aislamiento por `telegram_id`, cuotas, VPS.

**Decisiones tempranas:**
1. Qué modelo usar (probar con notas propias).
2. Una nota por PDF o por página (sugerido: por documento).
3. Dónde vive el vault (local o iCloud).

---

## 7. Extensión a varios usuarios (futuro)

- Un Mac solo sirve si está prendido: mover a un **VPS (~$4-6/mes)** con un proceso Python + cola SQLite.
- Carpeta aislada por usuario: `/data/users/<telegram_id>/{inbox, attachments, vault}`. Nunca construir rutas con texto del usuario.
- **Entrega de la nota** (el vault vive en el dispositivo de cada uno):
  1. El bot devuelve el `.md` por Telegram (más simple y barato).
  2. Sincronización por usuario (Syncthing, Dropbox, Drive API).
  3. Repo git por usuario con el plugin Obsidian Git.
- **Control de costos:** allowlist de IDs, cuota por usuario, BYOK (cada uno con su API key), límite de gasto, batch nocturno opcional.
- **Privacidad:** avisar que el contenido se envía al proveedor del modelo, borrar imágenes tras procesar y revisar la normativa de datos personales si se abre al público.
- Costo estimado: ~$5-8/mes para ~10 usuarios; menos con BYOK.

**Tip:** guardar `user_id` en la BD y las rutas desde el inicio facilita mucho la Fase 8.