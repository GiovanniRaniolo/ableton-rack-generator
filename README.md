
# 🎛️ AI Ableton Rack Generator (Live 12.3+)

> **Generate production-ready Audio Effect Racks from natural language prompts.**  
> *Now supporting the full Ableton Live 12.3 Standard/Suite arsenal (41+ Devices).*

![Status](https://img.shields.io/badge/Status-Stable-green) ![Ableton](https://img.shields.io/badge/Ableton-Live%2012.3-black) ![Python](https://img.shields.io/badge/Python-3.11+-blue) ![License](https://img.shields.io/badge/License-MIT-purple)

## 🚀 What is this?

This tool allows you to say:  
> *"Create a crunchy, lo-fi drum bus compressor with a bit of tape wobble and a resonant filter sweep mapped to a macro."*

And instantly get a **fully functional `.adg` file** (Ableton Device Group) that you can drag and drop directly into Live 12. No "forbidden icons", no crashes.

Unlike other generative tools that just randomize parameters, this engine understands **sound design semantics**. It knows that "Crunch" on a Drum Buss is different from "Drive" on an Overdrive, and it maps them intelligently to Macro Controls.

---

## 🏗️ Technical Pillars

### 1. 🧬 DNA Cloning Strategy (The "Forbidden Icon" Fix)
Ableton's `.adg` format is a complex, gzipped XML structure that changes between versions. Generating XML from scratch inevitably leads to corruption (the dreaded "Forbidden Icon").
**Our Solution:** We don't build devices from scratch. We **clone** the exact XML "DNA" of native devices (Roar, Reverb, Echo, etc.) from a validated Live 12.3 source file. The AI injects parameter values into these pristine shells, guaranteeing 100% compatibility.

### 2. 🧠 Grand Unified Semantic Map ("UX Expert Mode")
LLMs are great at creativity but bad at technical specificity. If an LLM suggests "Set Cutoff to 50%", a standard script fails because the internal parameter might be named `Stage1_Filter_Frequency` (Roar) or `Filter_Freq` (Auto Filter).
**Our Solution:** A comprehensive **Semantic Dictionary** maps human intent (Drive, Space, Wobble, Air) to the exact internal parameter ID for all 43 supported devices.
- "Spray" -> maps correctly to Grain Delay's `Spray`.
- "Frequency" -> maps correctly to Corpus' `Coarse` tune.

### 3. 🛡️ Safe Fallback System
The system is designed to never crash. If the AI hallucinates a device that doesn't exist (e.g. "SuperTube 3000"), the engine silently intercepts the request and substitutes a safe, sonic equivalent (e.g. `Saturator`), adding a "Ghost" tag to the logs but keeping the user's flow uninterrupted.

---

## 🔌 Supported Devices (The "Full Arsenal")
We support 41+ Native Audio Effects, including the new Live 12 additions:
- **Distortion:** **Roar**, Saturator, Overdrive, Pedal, Drum Buss, Redux, Vinyl Distortion...
- **Space:** **Hybrid Reverb**, **Spectral Time**, Echo, Grain Delay, Reverb...
- **Modulation:** **Auto Shift**, Phaser-Flanger, Chorus-Ensemble, Corpus...
- **Dynamics:** Glue Compressor, Multiband Dynamics, Limiter...

*(See `backend/data/cloned_devices_dna.json` for the raw DNA).*

---

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.11+
- Node.js (for Frontend)
- Ableton Live 12 Standard/Suite

### Quick Start
1.  **Clone the repo:**
    ```bash
    git clone https://github.com/GiovanniRaniolo/ableton-rack-generator.git
    cd ableton-rack-generator
    ```

2.  **Install Backend:**
    ```bash
    cd backend
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    Create a `.env` file in root or set your Google Gemini API key:
    ```
    GEMINI_API_KEY=your_key_here
    ```

4.  **Run:**
    ```bash
    # Windows
    .\run_backend.bat
    ```

5.  **Generate:**
    Use functionality via `curl` or the provided Frontend UI (coming soon).
    ```bash
    curl -X POST "http://localhost:8000/api/generate_rack" \
         -H "Content-Type: application/json" \
         -d '{"prompt": "A warm analog echo for dub techno chords"}'
    ```

---

## 🤝 Contributing

We welcome contributions! Whether it's adding "DNA" for Max for Live devices, improving the semantic map, or building a better UI.
See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up the dev environment.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---
*Built with ❤️ for the Ableton Community.*
