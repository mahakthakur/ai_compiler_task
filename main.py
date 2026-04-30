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

@server.post("/generate-website")
async def generate_website(request: dict):
    """Generate a simple website from user requirements."""
    description = request.get("description", "").strip()
    if not description:
        raise HTTPException(status_code=400, detail="No description provided")

    try:
        html = create_website_html(description)
        website_name = "-".join(description.split()[:3]).lower() or "website"
        website_name = website_name.replace("/", "-").replace("\\", "-")
        return {
            "html": html,
            "name": website_name,
            "description": description,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_website_html(description: str) -> str:
    """Build a website HTML document based on the user's description."""
    title = description[:60]
    subtitle = "A custom website generated from your software requirements."
    hero_cta = "See how it works"
    service_title = "Core Features"
    footer_text = "Generated with Nexus AI Compiler."

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title}</title>
    <script src=\"https://cdn.tailwindcss.com\"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; background-color: #0f172a; color: #e2e8f0; }}
    </style>
</head>
<body class=\"min-h-screen bg-gray-950 text-slate-100\">
    <nav class=\"max-w-7xl mx-auto px-6 py-5 flex items-center justify-between\">
        <div>
            <span class=\"text-xl font-bold text-white\">{description.split()[0] if description else 'Product'}</span>
        </div>
        <div class=\"space-x-6 text-slate-300 hidden md:flex\">
            <a href=\"#home\" class=\"hover:text-white transition\">Home</a>
            <a href=\"#features\" class=\"hover:text-white transition\">Features</a>
            <a href=\"#about\" class=\"hover:text-white transition\">About</a>
            <a href=\"#contact\" class=\"hover:text-white transition\">Contact</a>
        </div>
    </nav>

    <header id=\"home\" class=\"relative overflow-hidden bg-slate-950 py-24\">
        <div class=\"absolute inset-0 bg-gradient-to-br from-indigo-600/20 via-transparent to-purple-700/10 blur-3xl\"></div>
        <div class=\"relative max-w-7xl mx-auto px-6 text-center\">
            <p class=\"uppercase text-sm tracking-[0.4em] text-indigo-300 mb-6\">AI Generated Website</p>
            <h1 class=\"text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight text-white max-w-4xl mx-auto\">{title}</h1>
            <p class=\"max-w-3xl mx-auto text-slate-300 mt-6 text-lg sm:text-xl\">{subtitle}</p>
            <div class=\"mt-10 flex flex-col sm:flex-row justify-center gap-4\">
                <a href=\"#features\" class=\"inline-flex items-center justify-center rounded-full bg-indigo-600 px-8 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/20 hover:bg-indigo-500 transition\">{hero_cta}</a>
                <a href=\"#contact\" class=\"inline-flex items-center justify-center rounded-full border border-white/10 px-8 py-3 text-sm font-semibold text-slate-100 hover:bg-white/5 transition\">Contact Us</a>
            </div>
        </div>
    </header>

    <section id=\"features\" class=\"max-w-7xl mx-auto px-6 py-20\">
        <div class=\"grid gap-10 lg:grid-cols-3\">
            {generate_website_cards(description)}
        </div>
    </section>

    <section id=\"about\" class=\"bg-slate-900 py-20\">
        <div class=\"max-w-6xl mx-auto px-6 grid gap-10 lg:grid-cols-2 items-center\">
            <div class=\"space-y-6\">
                <h2 class=\"text-3xl font-bold text-white\">{service_title}</h2>
                <p class=\"text-slate-300 max-w-2xl\">This website is tailored to your requirements and includes modern design, clear sections, and conversion-focused content based on the description you provided.</p>
                <div class=\"grid gap-4 sm:grid-cols-2\">
                    <div class=\"rounded-3xl border border-white/10 bg-slate-950 p-6\">
                        <h3 class=\"font-semibold text-white mb-2\">Fast setup</h3>
                        <p class=\"text-slate-400 text-sm\">A responsive site structure ready for customization.</p>
                    </div>
                    <div class=\"rounded-3xl border border-white/10 bg-slate-950 p-6\">
                        <h3 class=\"font-semibold text-white mb-2\">Modern design</h3>
                        <p class=\"text-slate-400 text-sm\">Clean branding and professional layout for your product.</p>
                    </div>
                </div>
            </div>
            <div class=\"rounded-[2rem] border border-white/10 bg-slate-950 p-8 shadow-2xl shadow-indigo-500/10\">
                <h3 class=\"text-xl font-bold text-white mb-4\">{description}</h3>
                <ul class=\"space-y-4 text-slate-300\">
                    <li class=\"flex gap-3\"><span class=\"text-indigo-400\">•</span><span>Designed for your target audience and purpose.</span></li>
                    <li class=\"flex gap-3\"><span class=\"text-indigo-400\">•</span><span>Responsive layout for desktop and mobile.</span></li>
                    <li class=\"flex gap-3\"><span class=\"text-indigo-400\">•</span><span>Customizable content sections and calls to action.</span></li>
                </ul>
            </div>
        </div>
    </section>

    <section id=\"contact\" class=\"max-w-7xl mx-auto px-6 py-20\">
        <div class=\"rounded-[2rem] border border-white/10 bg-slate-950 p-10 shadow-2xl shadow-indigo-500/10\">
            <div class=\"flex flex-col gap-4 md:flex-row md:items-center md:justify-between\">
                <div>
                    <p class=\"text-indigo-400 uppercase tracking-[0.3em] text-xs\">Ready to launch</p>
                    <h2 class=\"text-3xl font-bold text-white\">Build your product with confidence.</h2>
                </div>
                <a href=\"mailto:hello@example.com\" class=\"inline-flex items-center justify-center rounded-full bg-purple-600 px-8 py-3 text-sm font-semibold text-white hover:bg-purple-500 transition\">Get in touch</a>
            </div>
        </div>
    </section>

    <footer class=\"border-t border-white/10 bg-slate-950 py-8\">
        <div class=\"max-w-7xl mx-auto px-6 text-center text-slate-500 text-sm\">{footer_text}</div>
    </footer>
</body>
</html>"""
    return html


def generate_website_cards(description: str) -> str:
    cards = [
        {"title": "Custom design", "text": "A polished layout that matches your needs."},
        {"title": "Easy navigation", "text": "Clear structure for faster user journeys."},
        {"title": "Conversion focus", "text": "Calls to action that guide visitors to your goal."},
    ]

    html = ""
    for card in cards:
        html += f"""
            <div class=\"rounded-3xl border border-white/10 bg-slate-950 p-8 shadow-lg shadow-slate-950/50\">
                <h3 class=\"text-xl font-semibold text-white mb-4\">{card['title']}</h3>
                <p class=\"text-slate-400\">{card['text']}</p>
            </div>
        """
    return html

# Run with: uvicorn fast:server --reload --host 0.0.0.0 --port 8000