
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
        
        # Create chains based on spec
        num_chains = spec.get("chains", 1)
        if num_chains < 1: num_chains = 1
        
        # If the AI suggested devices but only 1 chain, split them? 
        # Actually, let's follow the spec's logic. If chains > 1, we might need to distribute devices.
        # For now, let's create the requested number of chains.
        for i in range(num_chains):
            chain_name = f"Chain {i+1}" if num_chains > 1 else "Main Chain"
            chain = Chain(name=chain_name)
            
            # For the first chain (or if only 1), add all devices from spec
            # In a more advanced version, AI could specify which device goes to which chain
            if i == 0:
                for device_name in spec["devices"]:
                    try:
                        device = AbletonDevice(device_name, device_db)
                        chain.add_device(device)
                    except (ValueError, Exception) as e:
                        raise HTTPException(status_code=400, detail=f"Device '{device_name}' could not be initialized: {str(e)}")
            
            rack.add_chain(chain)
        
        # Set macro count
        rack.macro_count = request.macro_count or spec.get("macro_count", 8)
        
        # Auto-generate macro mappings using AI plan
        rack.auto_map_macros(spec.get("macro_details", []))
        
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
