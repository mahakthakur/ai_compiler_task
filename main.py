from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from compiler.workflow import app, generate_fallback_config
from compiler.evaluation import evaluate_system

server = FastAPI()

# Enable CORS so your frontend can connect
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@server.get("/")
async def read_index():
    return FileResponse("index.html")

@server.post("/compile")
async def compile_app(request: dict):
    user_prompt = request.get("prompt")
    if not user_prompt:
        raise HTTPException(status_code=400, detail="No prompt provided")
    
    try:
        # Run your LangGraph Compiler
        result = app.invoke({
            "user_input": user_prompt, 
            "error_log": None, 
            "is_valid": False
        })
        
        # Return the structured config to the frontend
        return result["config"].dict()
    except Exception as e:
        message = str(e)
        if 'Invalid API Key' in message or 'invalid_api_key' in message or 'Invalid API key' in message:
            fallback = generate_fallback_config(user_prompt)
            return fallback.dict()
        raise HTTPException(status_code=500, detail=message)

@server.post("/evaluate")
async def run_evaluation():
    """Run the evaluation framework and return results."""
    try:
        all_results, metrics = evaluate_system()
        return {"metrics": metrics, "results": all_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn fast:server --reload --host 0.0.0.0 --port 8000