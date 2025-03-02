import openai
from openai import OpenAI
from app.config import Config
from app.utils.errors import BadRequestError, ServiceUnavailableError


class OpenAIService:
    """Handles communication with OpenAI's API for text generation."""

    @staticmethod
    def generate_text(prompt: str) -> str:
        """
        Sends a prompt to OpenAI and returns the generated text.
        
        :param prompt: The input prompt for AI generation.
        :param max_tokens: The maximum number of tokens to generate.
        :return: The generated text response from OpenAI.
        :raises ServiceUnavailableError: If OpenAI API call fails.
        """
        try:
            client = OpenAI(
                api_key=Config.OPENAI_API_KEY
            )

            response = client.chat.completions.create(
                model="gpt-4o",
                store=True,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content
        
        except openai.OpenAIError as e:
            raise ServiceUnavailableError("OpenAI API is currently unavailable. Please try again later.", verboseMessage=str(e))

        except Exception as e:
            raise BadRequestError(str(e))