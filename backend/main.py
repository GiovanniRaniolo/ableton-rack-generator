
"""
Ableton Rack Generator - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
import time

from core.adg_builder import AudioEffectRack, Chain, AbletonDevice
from core.nlp_parser import RackNLPParser
from core.device_mapper import DeviceDatabase

# Initialize FastAPI app
app = FastAPI(
    title="Ableton Rack Generator API",
    description="Generate .adg Effect Racks from natural language",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
print("\n" + "="*50)
print(" STARTING NEW BACKEND INSTANCE (VQA FIXED) ")
print(f"Timestamp: {time.ctime()}")
print("="*50 + "\n")

device_db = DeviceDatabase()
nlp_parser = RackNLPParser(device_db)


# Models
class GenerateRequest(BaseModel):
    """Request model for rack generation"""
    prompt: str
    macro_count: Optional[int] = 8
    

class DeviceInfo(BaseModel):
    """Device information model"""
    name: str
    xml_tag: str
    type: str
    parameter_count: int


class RackInfo(BaseModel):
    """Generated rack information"""
    filename: str
    creative_name: str
    devices: List[str]
    macro_count: int
    chains: int
    sound_intent: Optional[str] = ""
    macro_details: Optional[List[dict]] = []
    parallel_logic: Optional[str] = ""
    tips: Optional[List[str]] = []
    explanation: Optional[str] = ""


# Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Ableton Rack Generator",
        "version": "1.0.0"
    }


@app.get("/devices", response_model=List[DeviceInfo])
async def list_devices():
    """Get list of available devices"""
    devices_list = device_db.get_all_devices()
    return [
        DeviceInfo(
            name=name,
            xml_tag=info["xml_tag"],
            type=info["type"],
            parameter_count=len(info.get("parameters", []))
        )
        for name, info in devices_list.items()
    ]


@app.post("/generate", response_model=RackInfo)
async def generate_rack(request: GenerateRequest):
    """
    Generate .adg file from natural language prompt
    """
    try:
        print(f"👉 RECEIVED REQUEST: {request.prompt}")
        
        # Parse prompt (now async for AI)
        spec = await nlp_parser.parse(request.prompt)
        print(f"🤖 AI PARSED: {spec['devices']}")
        
        if not spec["devices"]:
            raise HTTPException(
                status_code=400,
                detail="No devices found in prompt. Try: 'rack with compressor and EQ'"
            )
        
        # Create rack
        rack = AudioEffectRack(name="Custom Rack", device_db=device_db)
        
        # 3. Build chains based on topology and macro plan (V18 String-Strict Collection)
        all_required_devices = []
        
        # Extract from 'devices' list (can be [str] or [{"name": str}])
        for dev in spec.get("devices", []):
            d_name = dev.get("name") if isinstance(dev, dict) else dev
            if d_name and d_name not in all_required_devices:
                all_required_devices.append(d_name)
        
        # Extract from macro plan
        for plan_item in spec.get("macro_details", []):
            dev_name = plan_item.get("target_device")
            if dev_name and dev_name not in all_required_devices:
                all_required_devices.append(dev_name)
        
        # Extract from surgical_devices
        for s_dev in spec.get("surgical_devices", []):
            dev_name = s_dev.get("name")
            if dev_name and dev_name not in all_required_devices:
                all_required_devices.append(dev_name)

        num_chains = spec.get("chains", 1)
        if num_chains < 1: num_chains = 1
        
        # Parallel Distribution: If we have multiple chains, distribute devices
        for i in range(num_chains):
            chain_name = f"Chain {i+1}" if num_chains > 1 else "Main Chain"
            chain = Chain(name=chain_name)
            
            # Divide devices among chains if Parallel, otherwise put all in first chain
            if i == 0 or num_chains > 1:
                devices_for_this_chain = []
                if num_chains == 1:
                    devices_for_this_chain = all_required_devices
                else:
                    # Basic distribution: if we have 4 devices and 2 chains, put 2 in each
                    # Or just follow the first chain convention for now, but safer to distribute
                    chunk_size = max(1, len(all_required_devices) // num_chains)
                    start_idx = i * chunk_size
                    end_idx = start_idx + chunk_size if i < num_chains - 1 else len(all_required_devices)
                    devices_for_this_chain = all_required_devices[start_idx:end_idx]

                for device_name in devices_for_this_chain:
                    try:
                        device = AbletonDevice(device_name, device_db)
                        chain.add_device(device)
                    except Exception as e:
                        print(f"WARNING: Skipping device '{device_name}': {str(e)}")
            
            rack.add_chain(chain)
        
        # Set macro count
        rack.macro_count = request.macro_count or spec.get("macro_count", 8)
        
        # Auto-generate macro mappings and initialize parameters (Surgical V5)
        rack.auto_map_macros(spec)
        
        # Ensure 'generated' directory exists
        gen_dir = os.path.join(os.path.dirname(__file__), "generated")
        os.makedirs(gen_dir, exist_ok=True)
        
        # Generate filename based on creative name
        creative_name = spec.get("creative_name", "Custom Rack")
        clean_name = "".join(x for x in creative_name if x.isalnum() or x in " -_").replace(" ", "_")
        filename = f"{clean_name}_{os.urandom(2).hex()}.adg"
        filepath = os.path.join(gen_dir, filename)
        
        rack.save(filepath)
        print(f"✅ FILE GENERATED: {filename}")
        
        # Return info to frontend
        return RackInfo(
            filename=filename,
            creative_name=creative_name,
            devices=spec["devices"],
            macro_count=rack.macro_count,
            chains=len(rack.chains),
            sound_intent=spec.get("sound_intent", ""),
            macro_details=spec.get("macro_details", []),
            parallel_logic=spec.get("parallel_logic", ""),
            tips=spec.get("tips", []),
            explanation=spec.get("explanation", "")
        )
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_rack(filename: str):
    """Download a generated rack file"""
    gen_dir = os.path.join(os.path.dirname(__file__), "generated")
    filepath = os.path.join(gen_dir, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(
        filepath,
        media_type="application/octet-stream",
        filename=filename
    )


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "devices_loaded": device_db.device_count(),
        "nlp_ready": nlp_parser.is_ready()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
