#  AI Mock Interview Coach (Multi-Agent System)

A smart interview simulator that mimics real interview scenarios using **multiple AI agents** — designed to give **honest evaluation + actionable feedback**.

---


##  What this project does

This system conducts a full mock interview by:
- Asking adaptive questions  
- Evaluating answers in real-time  
- Providing structured, personalized feedback  

It behaves like a **real interviewer + evaluator + career coach combined**.

---


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

---


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

---



##  Key Highlights

- Multi-agent design (Interviewer + Evaluator + Coach)  
- Adaptive questioning based on performance  
- Structured scoring system (0–10 scale)  
- Actionable feedback (not generic advice)  
- Real interview-like experience  

---


##  Technical Design

- Local LLM-based system (no external API dependency)  
- Modular agent architecture  
- JSON-based structured outputs  
- Transcript logging for analysis  

---


##  What makes it different

**Most mock interview tools:**
- Give generic feedback  
- Don’t adapt to answers  

**This system:**
- Adjusts difficulty dynamically  
- Evaluates like a strict interviewer  
- Coaches like a real mentor  

---


##  Use Case

- Data Science / AI interview preparation  
- Practicing structured answers  
- Identifying real weaknesses before interviews  

---


##  Outcome

Helps candidates:

- Think clearly under pressure  
- Improve answer quality  
- Get interview-ready with targeted feedback

---

## Interview Transcripts


## Strong Candidate

Context: Role - Product Manager, Focus - Behavioral, Difficulty - Intermediate

Turn 1

Q: Tell me about a time you had to convince a team to adopt your idea.
A: At my previous company, I noticed our user onboarding had 40% drop-off. I proposed a redesign but engineering pushed back due to other priorities. I built a quick prototype, showed data from user sessions, and got buy-in from our VP. The redesign increased retention by 25%.

Score: 9/10 - Excellent STAR format, specific metrics, clear impact

Turn 2

Q: How did you handle the engineering team's initial resistance?
A: I scheduled one-on-ones with the lead engineer to understand their concerns. They were worried about timeline. I offered to reduce scope for v1 and handle user testing myself. We shipped in 3 weeks instead of 2 months.

Score: 8/10 - Good collaboration example, shows empathy

Interview Note

[Interview ends early at Turn 5 due to strong performance]

Final Feedback

Overall Score: 8.5/10
Strengths: Clear communication, metrics-driven, collaborative
Gaps: Could share more failure examples
Verdict: Yes - would hire

---

## Weak Candidate

Context: Role - Data Analyst, Focus - Technical, Difficulty - Beginner

Turn 1

Q: Explain how you would clean a dataset with missing values.
A: I would remove the missing rows.

Score: 4/10 - Too simplistic, missing other approaches

Turn 2

Q: What if removing rows removes too much data?
A: I don't know. Maybe fill with zeros?

Score: 3/10 - Basic understanding, lacks depth

Turn 3 (Probing deeper)

Q: When would you use median imputation instead of mean?
A: I think for skewed data? Not sure exactly.

Score: 3/10 - Partial knowledge, lacks confidence

Final Feedback

Overall Score: 3.5/10
Strengths: Honest when unsure, willing to attempt answers
Gaps: Limited knowledge of data cleaning techniques, lacks statistical fundamentals
Advice: Study pandas documentation, practice with Kaggle datasets
Verdict: No - needs significant technical preparation

---

## Edge Case - Vague Answers

Context: Role - Frontend Developer, Focus - Technical

Turn 1

Q: How would you optimize a slow React application?
A: I would make it faster by optimizing things.

Score: 2/10 - Extremely vague, no specific techniques

Turn 2 (Adapting - asking more specific question)

Q: Can you name one specific React hook or pattern you've used for performance?
A: useMemo? I've seen it in code but haven't used it much.

Score: 4/10 - Identified correct concept, lacks practical experience

Final Feedback

Overall Score: 3/10
Strengths: Recognizes basic concepts
Gaps: Cannot articulate specific solutions, lacks hands-on experience
Advice: Build a small React project focusing on useMemo, useCallback, and React.memo
Verdict: No - needs practical experience


---

## Key Design Decisions & Tradeoffs

### Decision 1: Local LLM over Cloud API
Why: The assignment requires a working POC. Using Ollama with local models makes this accessible to anyone without API costs or internet requirements.

Tradeoff: Local models are slower (5-15 seconds per response) but completely free and private.

### Decision 2: Separate Prompt Files
Why: The assignment specifically asks for a prompts/ folder with each agent's prompt as a separate file. This makes prompt engineering easier without touching code.

Tradeoff: More files to manage, but better separation of concerns.

### Decision 3: Real-time Evaluation
Why: To enable adaptive questioning, the system needs immediate feedback on each answer.

Tradeoff: Adds latency to each turn, but enables intelligent follow-ups and difficulty adjustment.

### Decision 4: Simple CLI over Web Interface
Why: The assignment says "simple CLI or notebook is fine." I chose CLI to minimize dependencies and keep focus on the agent architecture.

Tradeoff: Less polished UI, but faster to develop and test.

### Decision 5: JSON Outputs for Evaluator and Coach
Why: Structured data makes it easier to parse scores and generate consistent feedback.

Tradeoff: Requires careful prompt engineering to ensure valid JSON output.

