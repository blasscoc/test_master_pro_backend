from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from test_master_pro.models import GenerateRequest, GenerateResponse
from test_master_pro.generator import generate_markdown
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
import os

load_dotenv()


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


def verify_google_token(authorization: str = Header(...)):
    """
    Checks 'Authorization: Bearer <id_token>' header, verifies with Google.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split(" ")[1]
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            os.environ.get("GOOGLE_CLIENT_ID")
        )
        # Optionally check hosted domain, email, etc.
        return idinfo
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired Google token")

@app.get("/")
def root():
    return {"status": "ok", "message": "DOL Generator backend running"}

@app.post("/generate", response_model=GenerateResponse)
async def generate_test(req: GenerateRequest, user=Depends(verify_google_token)):
    """
    Generate a markdown DOL-style test given a list of TEKS codes.
    """
    markdown = await generate_markdown(req.teks_codes)
    return GenerateResponse(markdown=markdown)
