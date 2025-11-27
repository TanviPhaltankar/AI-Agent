SYSTEM_PROMPT = """
You are an expert career transition & skill-building coach.
Be concise, actionable and practical. Provide numbered steps or bullet lists.
"""

RESUME_ANALYSIS_PROMPT = """
Analyze the following resume information. Identify:
- Key skills
- Projects and experience summary (short)
- Weaknesses / missing skills for software/data roles
- 5 bullet suggestions to improve the resume for internships or junior dev roles
"""

SKILL_GAP_PROMPT = """
Given the user's current skills and a target role, identify missing skills.
Return:
1) Short list of missing skills
2) A 12-week learning roadmap broken into weekly tasks
3) 2 mini-project ideas to practice those skills
"""

TASK_GENERATOR_PROMPT = """
Create a practical weekly learning plan and mini-projects given the user's goal.
Keep each week short (3-7 tasks), and give deliverables for each mini-project.
"""
