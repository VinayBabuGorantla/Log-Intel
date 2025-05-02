class AppException(Exception):
    """Base class for custom exceptions."""
    def __init__(self, message="An application error occurred"):
        self.message = message
        super().__init__(self.message)

class FileTypeNotSupported(AppException):
    """Raised when an unsupported file type is uploaded."""
    def __init__(self, message="Unsupported file type provided"):
        super().__init__(message)

class LogProcessingError(AppException):
    """Raised when log file processing fails."""
    def __init__(self, message="Failed to process log file"):
        super().__init__(message)

class VectorStoreError(AppException):
    """Raised during vector DB operations."""
    def __init__(self, message="Vector store operation failed"):
        super().__init__(message)

class QAFailure(AppException):
    """Raised when the LLM fails to answer the query."""
    def __init__(self, message="Question answering failed"):
        super().__init__(message)
