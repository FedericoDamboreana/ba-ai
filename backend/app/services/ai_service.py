from openai import OpenAI
from app.config import settings
from typing import Dict, Any, Optional
import json


class AIService:
    """Service for interacting with OpenAI API."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL  # Model from environment variable

    def generate_structured_response(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Dict[str, Any],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate a structured response using OpenAI's structured outputs feature.

        Args:
            system_prompt: System message defining the AI's role
            user_prompt: User message with the task
            response_format: JSON schema for the expected response
            temperature: Sampling temperature (0-2), ignored for models that don't support it

        Returns:
            Parsed JSON response matching the schema

        Raises:
            Exception: If API call fails
        """
        try:
            # Prepare API call parameters
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "response",
                        "strict": True,
                        "schema": response_format
                    }
                }
            }

            # Only add temperature if not using gpt-5 (which only supports default)
            if not self.model.startswith("gpt-5"):
                params["temperature"] = temperature

            response = self.client.chat.completions.create(**params)

            # Parse the JSON response
            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            # Log error and re-raise with context
            print(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate AI response: {str(e)}")

    def generate_text_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a plain text response.

        Args:
            system_prompt: System message defining the AI's role
            user_prompt: User message with the task
            temperature: Sampling temperature (0-2), ignored for models that don't support it

        Returns:
            Plain text response

        Raises:
            Exception: If API call fails
        """
        try:
            # Prepare API call parameters
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }

            # Only add temperature if not using gpt-5 (which only supports default)
            if not self.model.startswith("gpt-5"):
                params["temperature"] = temperature

            response = self.client.chat.completions.create(**params)

            return response.choices[0].message.content

        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate AI response: {str(e)}")


# Global AI service instance
ai_service = AIService()
