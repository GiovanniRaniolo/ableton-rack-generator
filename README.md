# 🎹 Ableton Rack Generator

Generate Ableton Live Audio Effect Racks (`.adg` files) from natural language descriptions.

## 🚀 How to Start (The Right Way)


**Method 1: Automatic (Recommended)**
```powershell
.\start_dev.bat
```

**Method 2: Manual (Fail-Safe)**
If the automatic script freezes or fails, use these two separate scripts:
1. Double-click `run_backend.bat` (Keep this window open!)
2. Double-click `run_frontend.bat` (Keep this window open!)

---


---

## 🚀 Quick Start (Single Command)

Per avviare tutto il sistema (Backend + Frontend) con un solo comando:

1. Apri un terminale nella cartella root:
2. Esegui:
```bash
npm run dev
```

Questo comando avvierà:
- ✅ **API Backend** su `http://localhost:8000`
- ✅ **Frontend Web** su `http://localhost:5173`

---

### In caso di problemi (Esecuzione manuale):
Se il comando sopra non funziona, puoi avviarli separatamente:

#### 1. Avvia il Backend
```powershell
cd backend
python -m uvicorn main:app --reload --port 8000
```

#### 2. Avvia il Frontend
```powershell
cd frontend
npm run dev
```

### Prima installazione?
Se è la prima volta che scarichi la repo, installa prima le dipendenze:
```bash
npm install
cd backend
pip install -r requirements.txt
```

This starts:
- ✅ FastAPI backend on `http://localhost:8000`
- ✅ React frontend on `http://localhost:5173` (coming soon)

### 3. Test API

Open `http://localhost:8000/docs` for interactive API documentation.

#### Example Request:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Master chain with compressor, EQ and reverb",
    "macro_count": 8
  }'
```

#### Response:
Downloads `custom_rack.adg` ready for Ableton Live!

## 📁 Project Structure

```
ableton-rack-generator/
├── backend/              # FastAPI server
│   ├── main.py          # API endpoints
│   ├── core/
│   │   ├── adg_builder.py   # .adg XML generation
│   │   ├── nlp_parser.py    # Natural language parsing
│   │   └── device_mapper.py # Device database
│   └── data/
│       └── devices.json     # Device configurations
├── frontend/            # React app (coming soon)
└── package.json        # Root config with dev scripts
```

## 🎛️ Available Devices (45+)

Attualmente il generatore supporta tutti i principali effetti audio nativi di **Ableton Live 12 Suite**:

- **Dynamics**: Compressor, Glue Compressor, Limiter, Multiband Dynamics, Gate.
- **EQ & Filters**: EQ Eight, EQ Three, Channel EQ, Auto Filter.
- **Distortion & Saturation**: Roar (Live 12), Saturator, Overdrive, Erosion, Vinyl Distortion, Amp, Cabinet, Pedal, Dynamic Tube.
- **Modulation**: Chorus-Ensemble, Chorus, Phaser-Flanger, Phaser, Flanger, Auto Pan.
- **Drive & Delay**: Echo, Delay, Filter Delay, Grain Delay.
- **Reverb**: Hybrid Reverb, Reverb, Corpus.
- **Utilities & Others**: Utility (StereoGain), Redux (Modern & Legacy), Shifter, Spectral Time, Spectral Resonator, Vocoder, Resonators, Frequency Shifter, Spectrum, Tuner, Looper.

## 🧠 Natural Language Examples

```
"Master chain with compressor, EQ and reverb"
"Vocal rack: comp, eq, reverb"
"Creative FX with saturator and delay"
"Simple rack with EQ and filter"
```

## 📝 API Endpoints

- `GET /` - Health check
- `GET /devices` - List available devices
- `POST /generate` - Generate .adg file
- `GET /health` - Detailed health status

## 🔧 Development

### Backend Only:
```bash
npm run backend
```

### Frontend Only (when implemented):
```bash
npm run frontend
```

## 📦 Build for Production

```bash
npm run build
```

## 🎯 Roadmap

- [x] Backend API
- [x] Device database (45+ devices)
- [x] NLP parser (Gemini Integration)
- [x] .adg generation (Live 12.3 Parity)
- [x] Macro mapping for secret parameters
- [ ] React frontend (Phase 3)
- [ ] Multi-chain support (Parallel Chains)
- [ ] Preset templates

## 📄 License

MIT
