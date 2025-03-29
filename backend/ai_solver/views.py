from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
import os

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

class AIQuestionSolver(APIView):
    def post(self, request):
        """
        Endpoint to process student questions and return AI-generated solutions.
        """
        question = request.data.get("question", "")
        mode = request.data.get("mode", "step_by_step")  # Modes: step_by_step, hint, explanation
        
        if not question:
            return Response({"error": "Question is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Construct AI prompt based on selected mode
        prompt_templates = {
            "step_by_step": f"Solve this math problem step by step: {question}",
            "hint": f"Provide a hint to solve this math problem: {question}",
            "explanation": f"Explain the concept behind this math problem: {question}"
        }
        
        prompt = prompt_templates.get(mode, prompt_templates["step_by_step"])
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "system", "content": "You are a helpful math tutor."},
                          {"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            answer = response["choices"][0]["message"]["content"].strip()
            return Response({"question": question, "mode": mode, "solution": answer}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Failed to process the question.", "details": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
