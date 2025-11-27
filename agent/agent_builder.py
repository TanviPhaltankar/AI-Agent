# agent/agent_builder.py
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except Exception:
    genai = None

API_KEY = os.environ.get("GEMINI_API_KEY")

# Model names (from your account)
TEXT_MODEL = "models/gemini-2.5-flash"
VISION_MODEL = "models/gemini-2.5-flash-image"

# configure SDK if available
if genai and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception:
        pass


def _extract_text(resp):
    """Try common shapes to extract text safely."""
    try:
        if resp is None:
            return ""
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()
        try:
            return resp.output[0].content[0].text.strip()
        except Exception:
            pass
        try:
            return str(resp.candidates[0].output).strip()
        except Exception:
            pass
        return str(resp).strip()
    except Exception:
        return "Error extracting response."

def generate_answer(prompt: str) -> str:
    """
    Minimal, robust text-only wrapper that uses the GenerativeModel.generate_content call
    without extra kwargs that some SDK versions reject.
    """
    if not os.environ.get("GEMINI_API_KEY"):
        return "Gemini API key not set. Put GEMINI_API_KEY in your .env"

    try:
        # Use text-only model
        import google.generativeai as genai
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        resp = model.generate_content(prompt)   # no max_output_tokens kwarg
        # Try to return common response shapes
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()
        try:
            return resp.output[0].content[0].text.strip()
        except Exception:
            return str(resp).strip()
    except Exception as e:
        return f"Gemini Error: {e}"



def analyze_image_resume(image_path: str, max_output_tokens: int = 600) -> str:
    """
    Robust resume image analyzer that tries several call shapes for different SDK versions.
    Returns text or a helpful error string.
    """
    if not API_KEY:
        return "Gemini API key not set. Put GEMINI_API_KEY in your .env."

    if genai is None:
        return "google-generativeai SDK not installed. pip install google-generativeai"

    if not os.path.exists(image_path):
        return f"Resume image not found: {image_path}"

    prompt = (
        "You are an expert resume analyst. Analyze the resume image and produce concise bullets:\n"
        "- Key skills\n- Projects/experience summary (short)\n- Skill gaps for software roles\n- Five resume improvement suggestions\nKeep answers short and actionable."
    )

    last_err = None

    # read image once
    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()
    except Exception as e:
        return f"Could not read image file: {e}"

    # 1) Preferred: try model instance generate_content with max_output_tokens (some SDKs work)
    try:
        model = genai.GenerativeModel(VISION_MODEL)
        try:
            resp = model.generate_content([prompt, {"mime_type": "image/png", "data": img_bytes}], max_output_tokens=max_output_tokens)
            return _extract_text(resp)
        except TypeError as te:
            # SDK rejects the kwarg; retry without it
            try:
                resp = model.generate_content([prompt, {"mime_type": "image/png", "data": img_bytes}])
                return _extract_text(resp)
            except Exception as e2:
                last_err = f"Vision-model instance error (retry w/o max_output_tokens): {e2}"
        except Exception as e:
            last_err = f"Vision-model instance error: {e}"
    except Exception as e:
        last_err = f"Could not create model instance: {e}"

    # 2) Try genai.responses.generate (if present) with image input (different SDKs)
    try:
        if hasattr(genai, "responses") and hasattr(genai.responses, "generate"):
            try:
                resp = genai.responses.generate(
                    model=VISION_MODEL,
                    prompt=prompt,
                    input_image={"mime_type": "image/png", "data": img_bytes},
                    max_output_tokens=max_output_tokens,
                )
                return _extract_text(resp)
            except TypeError:
                # retry without the kwarg
                resp = genai.responses.generate(
                    model=VISION_MODEL,
                    prompt=prompt,
                    input_image={"mime_type": "image/png", "data": img_bytes},
                )
                return _extract_text(resp)
    except Exception as e:
        last_err = f"genai.responses.generate (image) error: {e}"

    # 3) Try older-style genai.generate_text with mixed content (if available)
    try:
        if hasattr(genai, "generate_text"):
            try:
                resp = genai.generate_text(model=VISION_MODEL, prompt=[prompt, {"mime_type": "image/png", "data": img_bytes}], max_output_tokens=max_output_tokens)
                return _extract_text(resp)
            except TypeError:
                resp = genai.generate_text(model=VISION_MODEL, prompt=[prompt, {"mime_type": "image/png", "data": img_bytes}])
                return _extract_text(resp)
    except Exception as e:
        last_err = f"genai.generate_text (image) error: {e}"

    # 4) All attempts failed — return a clear message and the last exception
    return (
        "Gemini Error (vision): all image methods failed.\n"
        "Possible causes: SDK version mismatch, model not supporting image input, or quota.\n"
        f"Last error: {last_err}\n\n"
        "If this persists, try upgrading the SDK:\n"
        "pip install --upgrade google-generativeai\n"
        "Then restart Streamlit and try again."
    )
