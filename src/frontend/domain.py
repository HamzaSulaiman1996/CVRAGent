import re
from typing import Any, Callable

import streamlit as st


def check_job_length(text, length: int = 100) -> bool:
    """
    Check if the job description is greater than the specified length.

    Args:
        text (str): The text to check.
        length (int): The minimum length.

    Returns:
        bool: True if the text is within the length limit, False otherwise.
    """

    return False if len(text) <= length else True


def format_output(output: str) -> str:
    # Remove <think>...</think> tags from deepseek model
    return re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL).strip()


@st.cache_resource(show_spinner=False)
def cache_function(_func: Callable[..., Any], **kwargs) -> Any:
    """
    Decorator to cache the resource.
    """
    return _func(**kwargs)
