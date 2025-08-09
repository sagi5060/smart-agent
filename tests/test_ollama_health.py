"""Tests for Ollama health check functionality."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from smart_agent.ollama_health import (
    DEFAULT_MODEL,
    OllamaHealthError,
    check_model_availability,
    check_ollama_service,
    get_available_models,
    validate_ollama_setup,
)


class TestOllamaHealthCheck:
    """Test suite for Ollama health check functions."""

    def test_check_ollama_service_running(self):
        """Test when Ollama service is running."""
        with patch("httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client.return_value.__enter__.return_value.get.return_value = (
                mock_response
            )

            assert check_ollama_service() is True

    def test_check_ollama_service_not_running(self):
        """Test when Ollama service is not running."""
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.get.side_effect = (
                httpx.RequestError("Connection failed")
            )

            assert check_ollama_service() is False

    def test_check_ollama_service_timeout(self):
        """Test when Ollama service times out."""
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.get.side_effect = (
                httpx.TimeoutException("Request timeout")
            )

            assert check_ollama_service() is False

    def test_check_model_availability_model_exists(self):
        """Test when required model is available."""
        with patch("smart_agent.ollama_health.Client") as mock_client:
            mock_models = MagicMock()
            mock_models.models = [
                MagicMock(model="llama3.1:8b"),
                MagicMock(model="codellama:7b"),
            ]
            mock_client.return_value.list.return_value = mock_models

            assert check_model_availability("llama3.1:8b") is True

    def test_check_model_availability_model_not_exists(self):
        """Test when required model is not available."""
        with patch("smart_agent.ollama_health.Client") as mock_client:
            mock_models = MagicMock()
            mock_models.models = [MagicMock(model="codellama:7b")]
            mock_client.return_value.list.return_value = mock_models

            assert check_model_availability("llama3.1:8b") is False

    def test_check_model_availability_client_error(self):
        """Test when Ollama client raises an error."""
        with patch("smart_agent.ollama_health.Client") as mock_client:
            mock_client.return_value.list.side_effect = Exception("Connection error")

            assert check_model_availability("llama3.1:8b") is False

    def test_get_available_models_success(self):
        """Test getting available models successfully."""
        with patch("smart_agent.ollama_health.Client") as mock_client:
            mock_models = MagicMock()
            mock_models.models = [
                MagicMock(model="llama3.1:8b"),
                MagicMock(model="codellama:7b"),
                MagicMock(model="mistral:7b"),
            ]
            mock_client.return_value.list.return_value = mock_models

            models = get_available_models()
            expected = ["llama3.1:8b", "codellama:7b", "mistral:7b"]
            assert models == expected

    def test_get_available_models_error(self):
        """Test getting available models when client fails."""
        with patch("smart_agent.ollama_health.Client") as mock_client:
            mock_client.return_value.list.side_effect = Exception("Connection error")

            models = get_available_models()
            assert models == []

    def test_validate_ollama_setup_success(self):
        """Test successful Ollama setup validation."""
        with (
            patch("smart_agent.ollama_health.check_ollama_service", return_value=True),
            patch(
                "smart_agent.ollama_health.check_model_availability", return_value=True
            ),
        ):
            # Should not raise any exception
            validate_ollama_setup()

    def test_validate_ollama_setup_service_not_running(self):
        """Test validation when Ollama service is not running."""
        with patch(
            "smart_agent.ollama_health.check_ollama_service", return_value=False
        ):
            with pytest.raises(OllamaHealthError) as exc_info:
                validate_ollama_setup()

            assert "Ollama service is not running" in str(exc_info.value)
            assert "ollama serve" in str(exc_info.value)

    def test_validate_ollama_setup_model_not_available(self):
        """Test validation when required model is not available."""
        with (
            patch("smart_agent.ollama_health.check_ollama_service", return_value=True),
            patch(
                "smart_agent.ollama_health.check_model_availability", return_value=False
            ),
            patch(
                "smart_agent.ollama_health.get_available_models",
                return_value=["codellama:7b"],
            ),
        ):
            with pytest.raises(OllamaHealthError) as exc_info:
                validate_ollama_setup()

            assert f"Required model '{DEFAULT_MODEL}' is not available" in str(
                exc_info.value
            )
            assert f"ollama pull {DEFAULT_MODEL}" in str(exc_info.value)
            assert "Available models: codellama:7b" in str(exc_info.value)

    def test_validate_ollama_setup_no_models_available(self):
        """Test validation when no models are available."""
        with (
            patch("smart_agent.ollama_health.check_ollama_service", return_value=True),
            patch(
                "smart_agent.ollama_health.check_model_availability", return_value=False
            ),
            patch("smart_agent.ollama_health.get_available_models", return_value=[]),
        ):
            with pytest.raises(OllamaHealthError) as exc_info:
                validate_ollama_setup()

            assert "No models are currently available" in str(exc_info.value)

    def test_validate_ollama_setup_custom_model(self):
        """Test validation with a custom model."""
        custom_model = "custom:7b"

        with (
            patch("smart_agent.ollama_health.check_ollama_service", return_value=True),
            patch(
                "smart_agent.ollama_health.check_model_availability", return_value=True
            ) as mock_check,
        ):
            validate_ollama_setup(custom_model)
            mock_check.assert_called_with(custom_model)
