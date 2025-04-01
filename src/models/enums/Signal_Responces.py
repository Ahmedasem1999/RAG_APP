from enum import Enum

class SignalResponces(Enum):
    """
    Enum class for signal responses.
    """
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_UPLOAD_FAILURE = "File upload failed."
    FILE_TYPE_INVALID = "Invalid file type."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."