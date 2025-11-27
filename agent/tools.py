# agent/tools.py
from agent.agent_builder import generate_answer, analyze_image_resume
import requests

def web_search(query: str) -> str:
    try:
        url = f"https://api.duckduckgo.com/?q={requests.utils.requote_uri(query)}&format=json"
        r = requests.get(url, timeout=6)
        data = r.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        if data.get("RelatedTopics"):
            return str(data["RelatedTopics"][0])[:1200]
        return "No concise web search result found."
    except Exception as e:
        return f"Web search failed: {e}"
# agent/tools.py (resume_analysis_tool - OCR fallback)
from PIL import Image
import pytesseract
from agent.agent_builder import generate_answer, analyze_image_resume  # if analyze_image_resume exists

def resume_analysis_tool(image_path: str) -> str:
    # 1) Try vision model first (if it succeeds we return its output)
    try:
        vision_resp = analyze_image_resume(image_path)
        if isinstance(vision_resp, str):
            low = vision_resp.lower()
            # If vision returned a quota or image error, fall back
            if "quota" in low or "429" in low or "vision" in low:
                pass
            else:
                return vision_resp
        else:
            return vision_resp
    except Exception:
        pass

    # 2) OCR fallback
    try:
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)
    except Exception as e:
        return f"OCR error: {e}"

    if not extracted_text.strip():
        return "OCR returned no text — try a clearer image or a PDF export."

    prompt = (
        "You are an expert resume analyst. Analyze the resume text and give concise bullets for:\n"
        "- Key skills and strengths\n- Projects/experience summary (short)\n- Top 3 skill gaps for software roles\n- Five resume improvements (ATS-friendly)\n\n"
        f"Resume text:\n{extracted_text}\n\nAnswer:"
    )
    return generate_answer(prompt)
    

def skill_gap_tool(user_input: str) -> str:
    prompt = (
        "You are an expert career coach. Identify missing skills and give a short weekly roadmap and two mini-project ideas.\n\n"
        f"User input:\n{user_input}\n\nAnswer:"
    )
    return generate_answer(prompt, max_output_tokens=400)

# inside agent/tools.py (replace the existing resume_analysis_tool)





def task_generator_tool(goal: str) -> str:
    prompt = (
        "You are an expert career coach. Produce a short weekly learning plan and two mini-project ideas.\n\n"
        f"Goal: {goal}\n\nAnswer:"
    )
    return generate_answer(prompt, max_output_tokens=400)
