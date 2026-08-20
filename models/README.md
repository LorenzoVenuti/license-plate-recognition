# Model weights

This pipeline uses two YOLO models:

| File | Role | Size | Where |
|------|------|------|-------|
| `LP.pt` | License-plate detection (YOLOv8n) | ~6 MB | committed here |
| `Ocr.pt` | Character recognition / OCR (YOLOv8l) | ~250 MB | GitHub Release asset |

`Ocr.pt` exceeds GitHub's 100 MB per-file limit, so it ships as an asset of the
[latest release](../../releases/latest) instead of being committed. Download it
and place it in this folder:

```bash
# from the repository root, with the GitHub CLI
gh release download --pattern Ocr.pt --dir models
```

Or download `Ocr.pt` manually from the Releases page and drop it into `models/`.
