"""
AI Mock Interview Coach - Multi-Agent System
Completely FREE - Uses local Ollama, no API key needed!
"""

import os
import json
from datetime import datetime
from typing import List, Dict

# Try to import Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print(" Ollama not installed. Run: pip install ollama")
    print(" Also download Ollama from https://ollama.com")
    exit(1)

# Local model configuration (FREE, no API key)
MODEL = "llama3.2"  # or "phi3:mini", "gemma3:latest", "mistral:latest"

# ============ LOCAL LLM CALL FUNCTION ============
def call_local_llm(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    """Call local Ollama model - completely free"""
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            options={"temperature": 0.7}
        )
        
        return response['message']['content']
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running (check system tray)")
        print(f"2. Download the model: ollama pull {MODEL}")
        print("3. Or try a smaller model: ollama pull phi3:mini")
        return ""


# ============ AGENT 1: INTERVIEWER ============
class InterviewerAgent:
    """Asks questions, adapts based on answers"""
    
    def __init__(self):
        self.system_prompt = """You are an expert interviewer. Your style is professional, conversational, and adaptive.

Rules:
- Ask ONE question at a time
- Mix question types based on focus area
- If candidate gave shallow answer, ask a follow-up probing question
- If candidate gave excellent answer, move to next topic
- Never repeat the same question type consecutively
- Keep questions concise (1-2 sentences)

For behavioral: Ask about specific situations (STAR format)
For technical: Test problem-solving, not just facts
For case: Present business scenarios
For mixed: Vary between all types"""
    
    def ask_question(self, context: Dict, history: List[Dict], difficulty: str) -> str:
        """Generate next question based on conversation history"""
        
        # Build history summary for context
        history_text = ""
        for turn in history[-3:]:  # Last 3 exchanges
            history_text += f"\nQ: {turn['question']}\nA: {turn['answer']}\nScore: {turn.get('score', 'N/A')}/10\n"
        
        user_prompt = f"""
Role: {context['role']}
Focus: {context['focus_area']}
Difficulty: {difficulty}
Candidate background: {context.get('background', 'Not provided')}

Previous conversation:
{history_text if history_text else "This is the first question."}

Generate the next interview question. Adapt based on their performance.
Be concise. Return ONLY the question.
"""
        
        response = call_local_llm(self.system_prompt, user_prompt)
        return response.strip() if response else f"Tell me about your experience with {context['role']}."


# ============ AGENT 2: EVALUATOR ============
class EvaluatorAgent:
    """Scores answers on multiple dimensions"""
    
    def __init__(self):
        self.system_prompt = """You are a strict but fair evaluator. Score answers honestly.

Scoring guidelines:
9-10: Exceptional (clear, specific, well-structured, confident)
7-8: Good (solid answer, minor gaps)
5-6: Average (answers question but lacking depth)
3-4: Weak (vague, off-topic, or very shallow)
0-2: Poor (doesn't answer, "I don't know", very wrong)

Return ONLY valid JSON. No other text."""
    
    def evaluate(self, question: str, answer: str, context: Dict) -> Dict:
        """Return structured evaluation"""
        
        user_prompt = f"""
Question: {question}
Answer: {answer}
Role: {context['role']}
Focus area: {context['focus_area']}

Return JSON with these fields:
{{
    "overall_score": 0-10,
    "relevance": 0-10,
    "clarity": 0-10,
    "depth": 0-10,
    "confidence": 0-10,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "feedback": "brief comment"
}}
"""
        
        response = call_local_llm(self.system_prompt, user_prompt)
        
        # Try to parse JSON
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback if JSON parsing fails
        return {
            "overall_score": 5,
            "relevance": 5,
            "clarity": 5,
            "depth": 5,
            "confidence": 5,
            "strengths": ["Attempted answer"],
            "weaknesses": ["Needs improvement"],
            "feedback": "Keep practicing!"
        }


# ============ AGENT 3: COACH ============
class CoachAgent:
    """Generates final feedback and improvement plan"""
    
    def __init__(self):
        self.system_prompt = """You are a supportive career coach. Your feedback should be actionable.

Structure your advice:
1. Start with genuine strengths (builds confidence)
2. Address specific gaps with examples from their answers
3. Give concrete action items (not generic "practice more")
4. Provide a clear 3-step practice plan

Return ONLY valid JSON. No other text."""
    
    def generate_feedback(self, transcript: List[Dict], context: Dict) -> Dict:
        """Comprehensive end-of-interview feedback"""
        
        # Format transcript
        transcript_text = ""
        for turn in transcript:
            transcript_text += f"""
Turn {turn['turn']}:
Q: {turn['question']}
A: {turn['answer']}
Score: {turn['score']}/10
Strengths: {', '.join(turn.get('strengths', []))}
Weaknesses: {', '.join(turn.get('weaknesses', []))}
"""
        
        user_prompt = f"""
Context:
- Target role: {context['role']}
- Focus area: {context['focus_area']}
- Difficulty used: {context.get('difficulty', 'intermediate')}

Full transcript:
{transcript_text}

Return JSON:
{{
    "overall_score": (average of all turns, 0-10),
    "strengths": ["top 3 strengths across all answers"],
    "gaps": ["top 3 areas needing improvement"],
    "specific_advice": "detailed paragraph of actionable advice",
    "practice_plan": "3 specific things to practice",
    "would_hire": "yes/no/maybe with brief reason"
}}
"""
        
        response = call_local_llm(self.system_prompt, user_prompt)
        
        # Try to parse JSON
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback feedback
        return {
            "overall_score": 5,
            "strengths": ["Attempted the interview"],
            "gaps": ["Need more preparation"],
            "specific_advice": "Practice answering interview questions clearly and concisely.",
            "practice_plan": "1. Review common questions\n2. Practice STAR method\n3. Record yourself",
            "would_hire": "maybe - needs more practice"
        }


# ============ ORCHESTRATOR ============
class InterviewOrchestrator:
    """Runs the multi-agent system"""
    
    def __init__(self):
        self.interviewer = InterviewerAgent()
        self.evaluator = EvaluatorAgent()
        self.coach = CoachAgent()
        self.transcript = []
    
    def run(self):
        print("\n" + "="*60)
        print("AI MOCK INTERVIEW COACH".center(60))
        print("Running on LOCAL Ollama - COMPLETELY FREE".center(60))
        print("="*60)
        
        # Check Ollama connection
        try:
            ollama.list()
            print(f"\n Connected to Ollama. Using model: {MODEL}")
        except:
            print(f"\nCannot connect to Ollama!")
            print("\nPlease:")
            print("1. Install Ollama from https://ollama.com")
            print(f"2. Run: ollama pull {MODEL}")
            print("3. Make sure Ollama is running in system tray")
            return
        
        # Get candidate info
        print("\n Let's set up your interview\n")
        role = input("Target role (e.g., Product Manager, Data Analyst): ").strip()
        background = input("Brief background (2-3 lines, optional): ").strip()
        
        print("\nFocus area:")
        print("  1. Behavioral")
        print("  2. Technical")
        print("  3. Case")
        print("  4. Mixed")
        focus_map = {"1": "behavioral", "2": "technical", "3": "case", "4": "mixed"}
        focus_choice = input("Choose (1-4): ").strip()
        focus_area = focus_map.get(focus_choice, "mixed")
        
        print("\nDifficulty:")
        print("  1. Beginner")
        print("  2. Intermediate")
        print("  3. Advanced")
        diff_choice = input("Choose (1-3): ").strip()
        difficulty_map = {"1": "beginner", "2": "intermediate", "3": "advanced"}
        difficulty = difficulty_map.get(diff_choice, "intermediate")
        
        context = {
            "role": role,
            "background": background,
            "focus_area": focus_area,
            "difficulty": difficulty
        }
        
        print("\n" + "="*60)
        print(" INTERVIEW STARTING".center(60))
        print("="*60)
        print("\n(Answer each question. Type 'exit' to end early)")
        print("  Responses may take 5-15 seconds (running locally)\n")
        
        # Run interview loop (5-7 turns)
        history = []
        for turn_num in range(1, 8):  # Max 7 turns
            print(f"\n--- Turn {turn_num} ---")
            
            # Generate question
            print(" Thinking...")
            question = self.interviewer.ask_question(context, history, difficulty)
            print(f"\n Interviewer: {question}")
            
            # Get answer
            answer = input("\n👤 You: ").strip()
            if answer.lower() == 'exit':
                print("\n Interview ended early.")
                break
            
            # Evaluate
            print(" Evaluating...")
            evaluation = self.evaluator.evaluate(question, answer, context)
            
            # Store
            turn_data = {
                "turn": turn_num,
                "question": question,
                "answer": answer,
                "score": evaluation["overall_score"],
                "strengths": evaluation.get("strengths", []),
                "weaknesses": evaluation.get("weaknesses", [])
            }
            history.append(turn_data)
            self.transcript.append(turn_data)
            
            # Show immediate feedback
            print(f"\n Score: {evaluation['overall_score']}/10 - {evaluation.get('feedback', '')}")
            
            # Adapt difficulty based on performance
            if evaluation["overall_score"] >= 8:
                difficulty = "advanced"
            elif evaluation["overall_score"] <= 4:
                difficulty = "beginner"
            else:
                difficulty = context["difficulty"]
            
            # Early exit conditions
            if turn_num >= 5 and evaluation["overall_score"] >= 8.5:
                print("\n You're doing great! I think we've seen enough.")
                break
            
            if turn_num >= 6 and evaluation["overall_score"] <= 3:
                print("\n Let's stop here and review where you can improve.")
                break
        
        # Generate final coaching
        print("\n" + "="*60)
        print(" GENERATING FEEDBACK".center(60))
        print("="*60)
        print(" Analyzing your responses...\n")
        
        feedback = self.coach.generate_feedback(self.transcript, context)
        
        # Display results
        print(f"\n OVERALL SCORE: {feedback.get('overall_score', 5)}/10")
        
        print(f"\nSTRENGTHS:")
        for s in feedback.get('strengths', ['Good effort']):
            print(f"   • {s}")
        
        print(f"\n AREAS TO IMPROVE:")
        for g in feedback.get('gaps', ['Keep practicing']):
            print(f"   • {g}")
        
        print(f"\n COACH'S ADVICE:")
        print(f"   {feedback.get('specific_advice', 'Practice more interview questions.')}")
        
        print(f"\n PRACTICE PLAN:")
        print(f"   {feedback.get('practice_plan', 'Review common questions in your field.')}")
        
        print(f"\n VERDICT: {feedback.get('would_hire', 'maybe')}")
        
        # Save transcript
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("transcripts", exist_ok=True)
        with open(f"transcripts/transcript_{timestamp}.json", "w") as f:
            json.dump({"context": context, "transcript": self.transcript, "feedback": feedback}, f, indent=2)
        print(f"\n Full transcript saved to transcripts/transcript_{timestamp}.json")


# ============ RUN ============
if __name__ == "__main__":
    print("\n Starting AI Mock Interview Coach...\n")
    coach = InterviewOrchestrator()
    coach.run()