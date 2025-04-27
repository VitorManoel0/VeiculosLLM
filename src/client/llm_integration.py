from os import getenv

from fastmcp.client.sampling import SamplingMessage, SamplingParams
from ollama import AsyncClient
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = getenv("OLLAMA_MODEL")
OLLAMA_HOST = getenv("OLLAMA_HOST", "http://ollama:11434")


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    ctx,
) -> str:
    """Handle sampling requests from the server using your preferred LLM."""
    # Extract the messages and system prompt
    prompt = [m.content.text for m in messages if m.content.type == "text"]
    system_instruction = params.systemPrompt or "You are a helpful assistant."

    # Configure Ollama client to use the Docker container
    ollama_client = AsyncClient(host=OLLAMA_HOST)

    # Prepare messages for Ollama
    formatted_messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": "\n".join(prompt)},
    ]

    try:
        response = await ollama_client.chat(
            model=OLLAMA_MODEL, messages=formatted_messages
        )
        return response.message.content
    except Exception as e:
        print(f"Erro ao conectar ao Ollama em {OLLAMA_HOST}: {str(e)}")
        raise
