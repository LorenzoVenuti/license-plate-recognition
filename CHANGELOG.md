# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioni: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-20

### Added
- Three-stage ANPR pipeline: plate detection (YOLOv8n), character OCR (YOLOv8l),
  coordinate-based character arrangement.
- Gradio GUI (`app.py`) and an end-to-end notebook (image + video).
- Detection weights `LP.pt` in the repository; OCR weights `Ocr.pt` as a release asset.
