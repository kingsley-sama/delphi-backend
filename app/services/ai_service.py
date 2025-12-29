import google.generativeai as genai
from core.config import settings
from typing import List, Dict, Any
import json
from models.quiz_model import QuizCreate, QuizQuestionCreate, DifficultyLevel, QuestionType

class AIQuizGenerator:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    async def generate_quiz(
        self,
        topic: str,
        subject: str,
        grade_level: int,
        num_questions: int = 10,
        difficulty: DifficultyLevel = DifficultyLevel.medium
    ) -> Dict[str, Any]:
        """
        Generate a quiz using AI based on topic and parameters
        """
        if not self.model:
            raise ValueError("Gemini API key not configured")
        
        prompt = self._build_prompt(topic, subject, grade_level, num_questions, difficulty)
        
        try:
            response = self.model.generate_content(prompt)
            quiz_data = self._parse_response(response.text)
            return quiz_data
        except Exception as e:
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    def _build_prompt(
        self,
        topic: str,
        subject: str,
        grade_level: int,
        num_questions: int,
        difficulty: DifficultyLevel
    ) -> str:
        """Build the prompt for AI quiz generation"""
        return f"""
You are an expert educational content creator. Generate a comprehensive quiz with the following specifications:

Topic: {topic}
Subject: {subject}
Grade Level: {grade_level}
Number of Questions: {num_questions}
Difficulty: {difficulty.value}

Please create a quiz with exactly {num_questions} questions. For each question, provide:
1. Question text
2. Question type (multiple_choice, true_false, or short_answer)
3. For multiple choice: 4 options labeled A, B, C, D
4. The correct answer
5. A brief explanation of why the answer is correct

Format your response as a JSON object with this structure:
{{
    "title": "Quiz title",
    "description": "Brief quiz description",
    "questions": [
        {{
            "question_text": "The question",
            "question_type": "multiple_choice",
            "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
            "correct_answer": "A",
            "explanation": "Why this is correct",
            "points": 1
        }}
    ]
}}

Make sure:
- Questions are age-appropriate for grade {grade_level}
- Questions test understanding, not just memorization
- Explanations are clear and educational
- Mix of question types if appropriate
- Questions progress from easier to harder
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response into structured quiz data"""
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[start_idx:end_idx]
            quiz_data = json.loads(json_str)
            
            # Validate structure
            if "title" not in quiz_data or "questions" not in quiz_data:
                raise ValueError("Invalid quiz structure")
            
            return quiz_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
    
    async def generate_personalized_quiz(
        self,
        user_performance_data: Dict[str, Any],
        topic: str,
        num_questions: int = 10
    ) -> Dict[str, Any]:
        """
        Generate a personalized quiz based on user's past performance
        """
        if not self.model:
            raise ValueError("Gemini API key not configured")
        
        weak_areas = user_performance_data.get("weak_areas", [])
        strong_areas = user_performance_data.get("strong_areas", [])
        average_score = user_performance_data.get("average_score", 70)
        
        prompt = f"""
You are an adaptive learning AI. Create a personalized quiz for a student with the following profile:

Topic: {topic}
Number of Questions: {num_questions}
Average Score: {average_score}%
Weak Areas: {', '.join(weak_areas) if weak_areas else 'None identified'}
Strong Areas: {', '.join(strong_areas) if strong_areas else 'None identified'}

Generate a quiz that:
1. Focuses 60% on weak areas to help improve
2. Includes 30% mixed difficulty questions
3. Has 10% challenging questions in strong areas
4. Adjusts difficulty based on average score (higher score = harder questions)

Use the same JSON format as before with title, description, and questions array.
"""
        
        try:
            response = self.model.generate_content(prompt)
            quiz_data = self._parse_response(response.text)
            return quiz_data
        except Exception as e:
            raise Exception(f"Failed to generate personalized quiz: {str(e)}")
    
    async def enhance_content(self, content: str, grade_level: int) -> str:
        """
        Enhance educational content using AI
        """
        if not self.model:
            raise ValueError("Gemini API key not configured")
        
        prompt = f"""
As an educational content expert, enhance the following content for grade {grade_level} students:

{content}

Improve it by:
1. Making it age-appropriate and engaging
2. Adding clear examples
3. Breaking down complex concepts
4. Including key takeaways
5. Maintaining accuracy

Return only the enhanced content, formatted in markdown.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to enhance content: {str(e)}")

# Initialize global instance
ai_quiz_generator = AIQuizGenerator()
