import openai
from app.config import Config, logging
from app.utils.errors import ServiceUnavailableError

class OpenAIService:
    """Handles communication with OpenAI's API for text generation."""

    @staticmethod
    def generate_text(prompt: str, max_tokens: int = 150, outputs: int = 1) -> str:
        """
        Sends a prompt to OpenAI and returns the generated text.
        
        :param prompt: The input prompt for AI generation.
        :param max_tokens: The maximum number of tokens to generate.
        :return: The generated text response from OpenAI.
        :raises ServiceUnavailableError: If OpenAI API call fails.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an AI assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                api_key=Config.OPENAI_API_KEY,
                n = outputs
            )

            logging.warning("OpenAI response object below!")
            logging.info(response)

            # return response.choices[0].message
            return response["choices"][0]["message"]["content"].strip()
        
        except openai.error.OpenAIError as e:
            raise ServiceUnavailableError("OpenAI API is currently unavailable. Please try again later.", verboseMessage=str(e))