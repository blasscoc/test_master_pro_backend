import os
import openai
from textwrap import dedent
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

SYSTEM_PROMPT = """
You are an expert Texas 3rd Grade Math teacher writing DOL (Demonstration of Learning),
CCFU, CADFA practice questions in markdown. 

Follow HISD style: short, challenging, full of trick language, TEKS-aligned.

Each question should be written as markdown checkboxes [- [ ] ...].
"""

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

async def generate_markdown(teks_codes):
    """
    Mocked version – in the real version this will call OpenAI ChatCompletion.
    """
    joined = ", ".join(teks_codes)

    # ✅ Replace this stub later with real GPT call
    return dedent(f"""
    # Grade 3 Mathematics – Auto Practice
    **TEKS Covered:** {joined}

    ---

    ### 1. Equal Groups
    There are **6 boxes**, each holding **8 apples**.  
    Which equation shows how many apples in total?

    - [ ] 6 + 8 = 14  
    - [ ] 6 × 8 = 48  
    - [ ] 8 ÷ 6 = 2  
    - [ ] 48 ÷ 6 = 8  

    ---

    ### 2. Trick Word Problem
    A gardener plants **5 equal rows of 7** flowers.  
    Which two equations represent the same situation?

    - [ ] 7 + 7 + 7 + 7 + 7 = 35  
    - [ ] 5 × 7 = 35  
    - [ ] 35 ÷ 5 = 7  
    - [ ] All of the above  

    ---
    **End of Test**
    """)


async def generate_markdown_openai(teks_codes):
    joined = ", ".join(teks_codes)
    completion = await openai.ChatCompletion.acreate(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a 3rd Grade math DOL for TEKS {joined} in markdown format."},
        ],
        temperature=1.0
    )
    return completion.choices[0].message.content
