
# Contributing to Ableton Rack Generator

Thank you for your interest in contributing! We want to make this the best open-source tool for Ableton users.

## 🛠️ Development Setup

The project consists of a **Python Backend** (FastAPI) and a **React Frontend** (Vite).

### 1. Environment Setup

**Backend:**
```bash
# From root
python -m venv .venv
.venv\Scripts\activate
# Install dev dependencies
pip install -r backend/requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Project Structure

- `backend/core/adg_builder.py`: **The Engine**. Contains the XML logic, GZIP handling, and the Semantic Map.
- `backend/core/nlp_parser.py`: **The Brain**. Handles the Gemini API interaction and prompt parsing.
- `backend/data/cloned_devices_dna.json`: **The DNA**. The database of verified XML structures for devices. **Do not manually edit this** unless you know what you are doing. Use `clone_devices.py` to extract new DNA.
- `backend/data/devices.json`: **The Metadata**. Contains parameter ranges and types.

### 3. Adding New Devices (Advanced)

If a new Ableton version releases a new device, we need to "clone" its DNA.
1. Create a simple `.adg` in Ableton containing ONLY the new device.
2. Save it as `analyze.adg` in the root.
3. Run:
   ```bash
   python clone_devices.py
   ```
4. This will extract the XML and append it to `cloned_devices_dna.json`.

### 4. Improving Semantic Mapping

Functionality relies on `SEMANTIC_MAP` in `adg_builder.py`.
If you find a macro that maps incorrectly (e.g. "Space" not mapping to Reverb Size):
1. Open `backend/core/adg_builder.py`.
2. Find the `SEMANTIC_MAP` dictionary.
3. Add the synonym to the relevant device entry.
   ```python
   "Reverb": {
       "space": "RoomSize", # Add this!
       ...
   }
   ```
4. Submit a Pull Request!

## 🧪 Testing

Before submitting, run a generation test to ensure no regressions:
```bash
curl -X POST "http://localhost:8000/api/generate_rack" ...
```
(We are working on a proper `pytest` suite - feel free to contribute one!)

## 📜 Code Style

- Python: Follow PEP 8.
- Commits: Use conventional commits (e.g. `feat: add Roar support`, `fix: macro mapping`).

Let's build something loud. 🔊
