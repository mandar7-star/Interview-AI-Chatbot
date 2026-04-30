#  AI Mock Interview Coach (Multi-Agent System)

A smart interview simulator that mimics real interview scenarios using **multiple AI agents** — designed to give **honest evaluation + actionable feedback**.




##  What this project does

This system conducts a full mock interview by:
- Asking adaptive questions  
- Evaluating answers in real-time  
- Providing structured, personalized feedback  

It behaves like a **real interviewer + evaluator + career coach combined**.




##  Core Idea

Instead of a single chatbot, this project uses a **multi-agent architecture** where each agent has a clear responsibility:

###  Interviewer Agent
- Asks one question at a time  
- Adapts based on previous answers  
- Mixes behavioral, technical, and case questions  

###  Evaluator Agent
- Scores answers on:
  - Clarity  
  - Relevance  
  - Depth  
  - Confidence  
- Identifies strengths and weaknesses  

###  Coach Agent
- Gives structured feedback:
  - Key strengths  
  - Improvement areas  
  - Actionable advice  
  - 3-step practice plan  
- Provides a final hiring recommendation  




##  Interview Flow

1. Candidate selects:
   - Role (e.g., Data Scientist)
   - Focus area (Behavioral / Technical / Mixed)
   - Difficulty level  

2. System runs **5–7 interview rounds**
   - Question → Answer → Evaluation  

3. Difficulty adapts dynamically:
   - Good answer → harder questions  
   - Weak answer → simpler questions  

4. Final output includes:
   - Overall score  
   - Strengths & gaps  
   - Personalized coaching feedback  





##  Key Highlights

- Multi-agent design (Interviewer + Evaluator + Coach)  
- Adaptive questioning based on performance  
- Structured scoring system (0–10 scale)  
- Actionable feedback (not generic advice)  
- Real interview-like experience  




##  Technical Design

- Local LLM-based system (no external API dependency)  
- Modular agent architecture  
- JSON-based structured outputs  
- Transcript logging for analysis  




##  What makes it different

**Most mock interview tools:**
- Give generic feedback  
- Don’t adapt to answers  

**This system:**
- Adjusts difficulty dynamically  
- Evaluates like a strict interviewer  
- Coaches like a real mentor  




##  Use Case

- Data Science / AI interview preparation  
- Practicing structured answers  
- Identifying real weaknesses before interviews  




##  Outcome

Helps candidates:

- Think clearly under pressure  
- Improve answer quality  
- Get interview-ready with targeted feedback




##  Sample Output

```json
{
  "overall_score": 6.4,
  "strengths": [
    "clear explanation of concepts",
    "good foundational understanding"
  ],
  "gaps": [
    "lack of depth",
    "missing real-world examples"
  ],
  "specific_advice": "Add examples and quantify your answers",
  "practice_plan": [
    "Practice SQL queries step-by-step",
    "Explain concepts using real datasets",
    "Improve structured answering (STAR method)"
  ],
  "would_hire": "maybe"
}
