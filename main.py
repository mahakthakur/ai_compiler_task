import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

# Aliasing 'app' to 'workflow_graph' to avoid conflict with the server
from compiler.workflow import app as workflow_graph, generate_fallback_config
from compiler.evaluation import evaluate_system

# 1. Initialize ONE server instance
app = FastAPI(title="AI Compiler API")

# 2. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Serve the Frontend (Root Route)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serves index.html from the local directory."""
    # Change "index.html" to whatever your actual filename is
    filename = "index.html" 
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.read()
    return "<h1>Backend Running</h1><p>Place your HTML file in this folder.</p>"

# 4. The Core AI Compiler Route
@app.post("/compile")
async def compile_app(request: dict):
    user_prompt = request.get("prompt")
    if not user_prompt:
        raise HTTPException(status_code=400, detail="No prompt provided")
    
    try:
        result = workflow_graph.invoke({
            "user_input": user_prompt, 
            "error_log": None, 
            "is_valid": False
        })
        
        if "config" not in result:
             raise ValueError("Compiler failed to generate a configuration.")

        return result["config"].dict()

    except Exception as e:
        message = str(e)
        if any(err in message.lower() for err in ['invalid api key', 'quota', 'rate limit']):
            fallback = generate_fallback_config(user_prompt)
            return fallback.dict()
        
        raise HTTPException(status_code=500, detail=message)

# 5. Evaluation Route
@app.post("/evaluate")
async def run_evaluation():
    try:
        all_results, metrics = evaluate_system()
        return {"metrics": metrics, "results": all_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))