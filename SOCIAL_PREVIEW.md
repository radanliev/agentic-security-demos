# Social Preview / Open Graph Banner Description

## Repository: agentic-security-demos

### OG Image Specifications
- **Dimensions**: 1280 x 640 pixels (2:1 aspect ratio)
- **Format**: PNG or JPEG
- **File size**: < 1 MB
- **Safe zone**: Center 1000 x 500 px (keep text/logo here)

---

### Visual Concept

**Background**: Dark gradient (indigo → purple) with subtle circuit/neural network pattern
- Left 60%: Dark indigo (#1e1b4b) → purple (#581c87) gradient
- Right 40%: Slightly lighter for text contrast

**Center Content** (within safe zone):
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│    🛡️  Agentic Security Demos                          │
│                                                         │
│    10 Hands-On Teaching Modules for Agentic AI Security │
│                                                         │
│    🎓  Undergrad → Grad Level    🛡️  Offline-First      │
│    🐍  Python 3.11+              🛡️  Zero Network       │
│                                                         │
│    github.com/radanliev/agentic-security-demos          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Visual Elements

**Icon/Logo** (left of title):
- Shield with circuit pattern (🛡️ style)
- Indigo/purple gradient fill
- 64x64 px minimum

**Typography**:
- Title: "Agentic Security Demos" — Bold, 48px, White
- Subtitle: "10 Hands-On Teaching Modules for Agentic AI Security" — Regular, 24px, Gray-300
- Badges: Pill-style, 16px, with icons
  - 🎓 Undergrad → Grad
  - 🛡️ Offline-First
  - 🐍 Python 3.11+
  - 🛡️ Zero Network

**Color Palette**:
- Primary: Indigo 600 (#4f46e5) / Indigo 700 (#4338ca)
- Accent: Purple 600 (#9333ea) / Purple 700 (#7e22ce)
- Background: Gray 900 (#111827) → Gray 800 (#1f2937)
- Text: White (#ffffff) / Gray-300 (#d1d5db)
- Accent Green: Emerald 500 (#10b981) for "pass" badges

---

### Alt Text (for accessibility)
"Agentic Security Demos — 10 hands-on teaching modules for agentic AI security. Offline-first, zero network, synthetic fixtures only. Python 3.11+, MIT licensed."

---

### Meta Tags for GitHub

```html
<!-- In repository settings → Social preview -->
<meta property="og:title" content="Agentic Security Demos — 10 Teaching Modules for Agentic AI Security" />
<meta property="og:description" content="10 hands-on, offline-first teaching modules for agentic AI security. Blind verification, AIBOM drift, evaluation invariants, authority confinement, evidence-backed release, network recon, malware triage, file inclusion, traffic interception, vulnerability scan control. All synthetic, zero network." />
<meta property="og:image" content="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/docs/assets/og-banner.png" />
<meta property="og:url" content="https://github.com/radanliev/agentic-security-demos" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Agentic Security Demos — 10 Teaching Modules for Agentic AI Security" />
<meta name="twitter:description" content="10 hands-on, offline-first teaching modules for agentic AI security." />
<meta name="twitter:image" content="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/docs/assets/og-banner.png" />
```

---

### Suggested Tools for Creation

| Tool | Best For |
|------|----------|
| **Figma** (free) | Vector design, component system |
| **Canva** | Quick templates, non-designers |
| **Excalidraw** | Hand-drawn style, open source |
| **Mermaid + CLI** | Diagram-based, version controlled |

---

### Quick Generation (CLI)

```bash
# Using ImageMagick (if installed)
convert -size 1280x640 gradient:#1e1b4b-#581c87 \
  -font "DejaVu-Sans-Bold" -pointsize 48 -fill white \
  -gravity center -annotate +0-60 "Agentic Security Demos" \
  -font "DejaVu-Sans" -pointsize 24 -fill "#d1d5db" \
  -gravity center -annotate +0+10 "10 Hands-On Teaching Modules for Agentic AI Security" \
  -font "DejaVu-Sans" -pointsize 16 -fill "#10b981" \
  -gravity center -annotate +0+70 "🎓 Undergrad → Grad  •  🛡️ Offline-First  •  🐍 Python 3.11+  •  🛡️ Zero Network" \
  og-banner.png
```

---

### File Location
```
docs/assets/og-banner.png  (add to git)
```

**Reference in mkdocs.yml**:
```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/radanliev/agentic-security-demos
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

---

*Template version: 1.0 | Create once, update rarely*