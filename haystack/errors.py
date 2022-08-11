"""Custom Errors for Haystack"""

from typing import Optional

from haystack.telemetry import send_custom_event


class HaystackError(Exception):
    """
    Any error generated by Haystack.

    This error wraps its source transparently in such a way that its attributes
    can be accessed directly: for example, if the original error has a `message` attribute,
    `HaystackError.message` will exist and have the expected content.
    """

    def __init__(self, message: Optional[str] = None, docs_link: Optional[str] = None):
        send_custom_event(event=f"{type(self).__name__} raised")
        super().__init__()
        if message:
            self.message = message
        self.docs_link = None

    def __getattr__(self, attr):
        # If self.__cause__ is None, it will raise the expected AttributeError
        getattr(self.__cause__, attr)

    def __str__(self):
        if self.docs_link:
            docs_message = f"\n\nCheck out the documentation at {self.docs_link}"
            return self.message + docs_message
        return self.message

    def __repr__(self):
        return str(self)


class ModelingError(HaystackError):
    """Exception for issues raised by the modeling module"""

    def __init__(self, message: Optional[str] = None, docs_link: Optional[str] = "https://haystack.deepset.ai/"):
        super().__init__(message=message, docs_link=docs_link)


class PipelineError(HaystackError):
    """Exception for issues raised within a pipeline"""

    def __init__(
        self, message: Optional[str] = None, docs_link: Optional[str] = "https://haystack.deepset.ai/pipelines"
    ):
        super().__init__(message=message, docs_link=docs_link)


class PipelineSchemaError(PipelineError):
    """Exception for issues arising when reading/building the JSON schema of pipelines"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class PipelineConfigError(PipelineError):
    """Exception for issues raised within a pipeline's config file"""

    def __init__(
        self,
        message: Optional[str] = None,
        docs_link: Optional[str] = "https://haystack.deepset.ai/pipelines#yaml-file-definitions",
    ):
        super().__init__(message=message, docs_link=docs_link)


class DocumentStoreError(HaystackError):
    """Exception for issues that occur in a document store"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class DuplicateDocumentError(DocumentStoreError, ValueError):
    """Exception for Duplicate document"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class NodeError(HaystackError):
    """Exception for issues that occur in a node"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class AudioNodeError(NodeError):
    """Exception for issues that occur in a node of the audio module"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class OpenAIError(NodeError):
    """Exception for issues that occur in the OpenAI Answer Generator node"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)
