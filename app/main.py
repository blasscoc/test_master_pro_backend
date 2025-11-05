from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test_master_pro.models import GenerateRequest, GenerateResponse
from test_master_pro.generator import generate_markdown


app = FastAPI(
    title="HISD Test Generator API",
    description="Generates markdown practice tests aligned with TEKS using GPT.",
    version="0.1.0",
)

# Allow your frontend (Vite/React) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "DOL Generator backend running"}

@app.post("/generate", response_model=GenerateResponse)
async def generate_test(req: GenerateRequest):
    """
    Generate a markdown DOL-style test given a list of TEKS codes.
    """
    markdown = await generate_markdown(req.teks_codes)
    return GenerateResponse(markdown=markdown)
