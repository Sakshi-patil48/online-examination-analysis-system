import os
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def evaluate_short_answer(question_text: str, model_answer: str, student_answer: str, max_marks: float = 1.0) -> Dict[str, Any]:
    """
    Evaluates student's short answer against the model answer.
    First attempts Gemini AI if API key is present.
    Falls back deterministically to fuzzy keyword matching if Gemini is unconfigured or fails.
    """
    if not student_answer or not student_answer.strip():
        return {
            'is_correct': False,
            'score_obtained': 0.0,
            'confidence': 100.0,
            'explanation': 'No answer was provided.',
            'evaluation_method': 'KEYWORD_FALLBACK'
        }

    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an expert academic evaluator grading a student's answer.

            Question: {question_text}
            Model/Key Reference Answer: {model_answer}
            Student Answer: {student_answer}
            Maximum Score: {max_marks}

            Evaluate the student's answer based on conceptual accuracy, correctness, and key point coverage.
            Respond strictly in valid JSON format with the following keys:
            - "is_correct": boolean (true if student score >= 50% of max_marks)
            - "score_obtained": float (number between 0 and {max_marks})
            - "confidence": float (percentage confidence between 0 and 100)
            - "explanation": string (1-2 sentences explaining why this score was awarded)
            """
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            raw_text = response.text.strip()
            # Attempt to parse JSON from response
            import json
            clean_json = raw_text.replace('```json', '').replace('```', '').strip()
            res = json.loads(clean_json)
            return {
                'is_correct': bool(res.get('is_correct', False)),
                'score_obtained': min(float(res.get('score_obtained', 0.0)), float(max_marks)),
                'confidence': float(res.get('confidence', 90.0)),
                'explanation': str(res.get('explanation', 'Evaluated via Gemini AI.')),
                'evaluation_method': 'GEMINI'
            }
        except Exception as e:
            logger.warning(f"Gemini API evaluation failed or unconfigured, falling back: {e}")

    # Fallback evaluation algorithm: Keyword & Token Overlap matching
    return fallback_keyword_matching(question_text, model_answer, student_answer, max_marks)

def fallback_keyword_matching(question_text: str, model_answer: str, student_answer: str, max_marks: float) -> Dict[str, Any]:
    """
    Deterministic keyword & n-gram overlap evaluator.
    Calculates overlap ratio of important terms in model answer.
    """
    def tokenize(text: str):
        words = re.findall(r'\b\w+\b', text.lower())
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'that', 'this', 'it'}
        return [w for w in words if w not in stopwords]

    model_tokens = set(tokenize(model_answer))
    student_tokens = set(tokenize(student_answer))

    if not model_tokens:
        overlap_ratio = 1.0 if student_tokens else 0.0
    else:
        matched = model_tokens.intersection(student_tokens)
        overlap_ratio = len(matched) / len(model_tokens)

    # Calculate score
    score = round(overlap_ratio * float(max_marks), 2)
    is_correct = overlap_ratio >= 0.5
    confidence = min(round(overlap_ratio * 100, 1), 85.0)

    explanation = f"Evaluated via Keyword Matching algorithm. Matched {int(overlap_ratio * 100)}% of core reference terms."

    return {
        'is_correct': is_correct,
        'score_obtained': score,
        'confidence': max(confidence, 50.0),
        'explanation': explanation,
        'evaluation_method': 'KEYWORD_FALLBACK'
    }
