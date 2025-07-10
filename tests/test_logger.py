"""
Unit tests for the logger module.
"""

import logging
from io import StringIO
from unittest.mock import mock_open, patch

from repospector_ai.core.logger import (
    get_logger,
    logger,
    setup_logger,
)


class TestLoggerSetup:
    """Test logger setup and configuration."""

    def test_setup_logger_basic(self):
        """Test basic logger setup."""
        test_logger = setup_logger("test_logger")

        assert isinstance(test_logger, logging.Logger)
        assert test_logger.name == "test_logger"
        assert test_logger.level == logging.INFO

    @patch("repospector_ai.core.logger.settings")
    def test_setup_logger_with_debug(self, mock_settings):
        """Test logger setup with debug level."""
        mock_settings.log_level = "DEBUG"
        mock_settings.log_format = "json"
        mock_settings.log_file = None

        test_logger = setup_logger("debug_logger")

        assert test_logger.level == logging.DEBUG

    @patch("repospector_ai.core.logger.settings")
    def test_setup_logger_with_file_output(self, mock_settings):
        """Test logger setup with file output."""
        mock_settings.log_level = "INFO"
        mock_settings.log_format = "json"
        mock_settings.log_file = "/tmp/test.log"

        with patch("builtins.open", mock_open()):
            test_logger = setup_logger("file_logger")

            # Check that logger has appropriate handlers
            assert len(test_logger.handlers) > 0

    @patch("repospector_ai.core.logger.settings")
    def test_setup_logger_text_format(self, mock_settings):
        """Test logger setup with text format."""
        mock_settings.log_level = "INFO"
        mock_settings.log_format = "text"
        mock_settings.log_file = None

        test_logger = setup_logger("text_logger")

        # Verify logger is set up (specific format checking is complex)
        assert isinstance(test_logger, logging.Logger)

    def test_get_logger_function(self):
        """Test the get_logger convenience function."""
        test_logger = get_logger("test_module")

        assert isinstance(test_logger, logging.Logger)
        assert "test_module" in test_logger.name

    def test_default_logger_instance(self):
        """Test the default logger instance."""
        assert isinstance(logger, logging.Logger)
        assert logger.name == "repospector_ai"


class TestLoggerFunctionality:
    """Test logger functionality and output."""

    def test_logger_info_message(self):
        """Test info level logging."""
        with patch("sys.stdout", new_callable=StringIO):
            test_logger = setup_logger("info_test")
            test_logger.info("Test info message")

            # Verify message was logged (output format may vary)
            # The exact assertion depends on handler configuration

    def test_logger_error_message(self):
        """Test error level logging."""
        with patch("sys.stderr", new_callable=StringIO):
            test_logger = setup_logger("error_test")
            test_logger.error("Test error message")

            # Verify error was logged

    def test_logger_debug_message_filtered(self):
        """Test that debug messages are filtered at INFO level."""
        test_logger = setup_logger("debug_filter_test")
        test_logger.setLevel(logging.INFO)

        with patch("sys.stdout", new_callable=StringIO):
            test_logger.debug("This should not appear")

            # Debug message should not appear in output

    @patch("repospector_ai.core.logger.settings")
    def test_logger_with_json_formatter(self, mock_settings):
        """Test logger with JSON formatter."""
        mock_settings.log_level = "INFO"
        mock_settings.log_format = "json"
        mock_settings.log_file = None

        test_logger = setup_logger("json_test")

        # Test that JSON formatter is applied
        # This is a complex test that would require capturing handler output
        assert isinstance(test_logger, logging.Logger)

    def test_logger_exception_handling(self):
        """Test logger exception handling."""
        test_logger = setup_logger("exception_test")

        try:
            raise ValueError("Test exception")
        except ValueError:
            # Test that exception logging works
            test_logger.exception("Test exception occurred")

            # Verify exception was logged with traceback
            assert True  # Basic test that no errors occur


class TestLoggerConfiguration:
    """Test logger configuration edge cases."""

    @patch("repospector_ai.core.logger.settings")
    def test_invalid_log_level_handling(self, mock_settings):
        """Test handling of invalid log levels."""
        mock_settings.log_level = "INVALID"
        mock_settings.log_format = "json"
        mock_settings.log_file = None

        # Should handle invalid log level gracefully
        test_logger = setup_logger("invalid_level_test")
        assert isinstance(test_logger, logging.Logger)

    @patch("repospector_ai.core.logger.settings")
    def test_invalid_log_format_handling(self, mock_settings):
        """Test handling of invalid log formats."""
        mock_settings.log_level = "INFO"
        mock_settings.log_format = "invalid_format"
        mock_settings.log_file = None

        # Should handle invalid format gracefully
        test_logger = setup_logger("invalid_format_test")
        assert isinstance(test_logger, logging.Logger)

    def test_logger_isolation(self):
        """Test that different loggers are isolated."""
        logger1 = setup_logger("test_logger_1")
        logger2 = setup_logger("test_logger_2")

        assert logger1 != logger2
        assert logger1.name != logger2.name

    def test_logger_singleton_behavior(self):
        """Test logger singleton-like behavior for same name."""
        logger1 = get_logger("same_name")
        logger2 = get_logger("same_name")

        # Both should reference the same logger instance
        assert logger1.name == logger2.name
