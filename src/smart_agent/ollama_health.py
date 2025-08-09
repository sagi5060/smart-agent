"""Ollama health check utilities."""

import logging

import httpx

from ollama import AsyncClient, Client

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"


class OllamaHealthError(Exception):
    """Raised when Ollama service or model is not available."""

    pass


def check_ollama_service() -> bool:
    """Check if Ollama service is running and accessible.

    Returns:
        bool: True if service is running, False otherwise
    """
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{OLLAMA_BASE_URL}/api/version")
            return response.status_code == 200
    except (httpx.RequestError, httpx.TimeoutException):
        return False


def check_model_availability(model_name: str = DEFAULT_MODEL) -> bool:
    """Check if the specified model is available in Ollama.

    Args:
        model_name: Name of the model to check (default: llama3.1:8b)

    Returns:
        bool: True if model is available, False otherwise
    """
    try:
        client = Client()
        models = client.list()
        available_models = [
            model.model for model in models.models if model.model is not None
        ]
        return model_name in available_models
    except Exception:
        return False


async def check_model_availability_async(model_name: str = DEFAULT_MODEL) -> bool:
    """Async version of check_model_availability.

    Args:
        model_name: Name of the model to check (default: llama3.1:8b)

    Returns:
        bool: True if model is available, False otherwise
    """
    try:
        client = AsyncClient()
        models = await client.list()
        available_models = [
            model.model for model in models.models if model.model is not None
        ]
        return model_name in available_models
    except Exception:
        return False


def get_available_models() -> list[str]:
    """Get list of available models in Ollama.

    Returns:
        list[str]: List of available model names
    """
    try:
        client = Client()
        models = client.list()
        return [model.model for model in models.models if model.model is not None]
    except Exception:
        return []


def validate_ollama_setup(model_name: str = DEFAULT_MODEL) -> None:
    """Validate that Ollama is running and the required model is available.

    Args:
        model_name: Name of the model to check (default: llama3.1:8b)

    Raises:
        OllamaHealthError: If Ollama service is not running or model is not available
    """
    # Check if Ollama service is running
    if not check_ollama_service():
        raise OllamaHealthError(
            f"Ollama service is not running or not accessible at {OLLAMA_BASE_URL}.\n"
            "Please ensure Ollama is installed and running:\n"
            "  1. Install Ollama: https://ollama.ai/\n"
            "  2. Start Ollama service: 'ollama serve'\n"
            "  3. Verify service: 'curl http://localhost:11434/api/version'"
        )

    # Check if the required model is available
    if not check_model_availability(model_name):
        available_models = get_available_models()
        error_msg = (
            f"Required model '{model_name}' is not available in Ollama.\n"
            "Please pull the model first:\n"
            f"  ollama pull {model_name}\n"
        )

        if available_models:
            error_msg += f"\nAvailable models: {', '.join(available_models)}"
        else:
            error_msg += (
                "\nNo models are currently available. Please pull at least one model."
            )

        raise OllamaHealthError(error_msg)

    logger.info(
        f"Ollama health check passed - service running, model '{model_name}' available"
    )


async def validate_ollama_setup_async(model_name: str = DEFAULT_MODEL) -> None:
    """Async version of validate_ollama_setup.

    Args:
        model_name: Name of the model to check (default: llama3.1:8b)

    Raises:
        OllamaHealthError: If Ollama service is not running or model is not available
    """
    # Check if Ollama service is running
    if not check_ollama_service():
        raise OllamaHealthError(
            f"Ollama service is not running or not accessible at {OLLAMA_BASE_URL}.\n"
            "Please ensure Ollama is installed and running:\n"
            "  1. Install Ollama: https://ollama.ai/\n"
            "  2. Start Ollama service: 'ollama serve'\n"
            "  3. Or use Docker with pre-built model: 'docker run -d -p 11434:11434 ollama/ollama:latest'\n"
            "  4. Verify service: 'curl http://localhost:11434/api/version'"
        )

    # Check if the required model is available
    if not await check_model_availability_async(model_name):
        available_models = get_available_models()
        error_msg = (
            f"Required model '{model_name}' is not available in Ollama.\n"
            "Please pull the model first:\n"
            f"  ollama pull {model_name}\n"
        )

        if available_models:
            error_msg += f"\nAvailable models: {', '.join(available_models)}"
        else:
            error_msg += (
                "\nNo models are currently available. Please pull at least one model."
            )

        raise OllamaHealthError(error_msg)

    logger.info(
        f"Ollama health check passed - service running, model '{model_name}' available"
    )
