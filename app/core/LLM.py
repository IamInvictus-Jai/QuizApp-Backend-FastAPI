from openai import OpenAI
from app.schema.exceptions import FailedToGenerateResponse, FailedToGenerateNotes
from app.config.settings import Settings
from app.utils.readInstructions import LoadInstructions

class LLM:
    def __init__(self, loader:LoadInstructions, settings:Settings) -> None:
        self.loader = loader
        self.settings = settings

        self.functions = self.loader.load('functions.json')
        self.fallback_instructions = self.loader.load('fallback_instructions.txt')

        self.GPT_MODEL = self.settings.GPT_MODEL
        self.openai = OpenAI(api_key=self.settings.OPENAI_API_KEY)
    
    def generate_content(self, user_prompt:str, system_prompt:str, use_func_call:bool = False):

        try:
            response = self.openai.chat.completions.create(
                model=self.GPT_MODEL,  # or "gpt-3.5-turbo" for a cheaper but less capable model
                messages=[
                    {"role": "system", "content":system_prompt},
                    {"role": "user", "content":user_prompt}
                ],
                max_tokens=4000,
                temperature=0.7,

                # Use function calling when reponse_format is also not parsing the response correctly ( function call supported by few models only -> gpt-3.5-turbo-1106 , gpt-4o)
                functions= self.functions if use_func_call else None,
                function_call={"name": "generate_quiz"} if use_func_call else None
            )

            if not response:
                raise FailedToGenerateResponse("No response received from OpenAI API. Please check your API key and try again.")

            if use_func_call:
                return response.choices[0].message.function_call.arguments
            return response.choices[0].message.content
        
        except Exception as e:
            raise FailedToGenerateResponse(e)

    def fallback_generate_content(self, prev_response):
        try:
            response = self.openai.chat.completions.create(
                model=self.GPT_MODEL,  # or "gpt-3.5-turbo" for a cheaper but less capable model
                messages=[
                    {"role": "system", "content": self.fallback_instructions},
                    {"role": "user", "content": prev_response}
                ],
                max_tokens=4000,
                temperature=0.7,

                # Use function calling when reponse_format is also not parsing the response correctly ( function call supported by few models only -> gpt-3.5-turbo-1106 , gpt-4o)
                functions=self.functions,
                function_call={"name": "generate_quiz"}
            )

            if not response:
                raise FailedToGenerateNotes("No response received from OpenAI API. Please check your API key and try again.")
            
            return response.choices[0].message.function_call.arguments
        except Exception as e:
            raise FailedToGenerateResponse(e)