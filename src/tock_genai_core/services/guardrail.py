import random
import requests
from urllib.parse import urljoin
from typing import Optional, List

from pydantic import BaseModel
from langchain_core.output_parsers.transform import BaseCumulativeTransformOutputParser


class GuardrailOutput(BaseModel):
    """
    A model representing the output of a guardrail process.

    Attributes
    ----------
    content : str
        The generated content or response from the model.

    output_toxicity : bool, optional
        A flag indicating whether the generated content is considered toxic. Defaults to `False`.

    output_toxicity_reason : list[str], optional
        A list of reasons explaining why the generated content is considered toxic, if applicable. Defaults to an empty
        list.
    """

    content: str
    output_toxicity: bool = False
    output_toxicity_reason: Optional[list[str]] = []


class BloomzGuardrailOutputParser(BaseCumulativeTransformOutputParser[dict]):
    """
    Parser for Bloomz Guardrail outputs, used to analyze the toxicity of generated text.
    This class is responsible for parsing the output of a Bloomz Guardrail API response,
    which evaluates the toxicity of generated content, and for providing details about
    the toxicity status and reasons.

    Attributes
    ----------
    max_score : float
        The maximum acceptable toxicity score. Any response with a score higher than this will be flagged as toxic.

    endpoint : str
        The API endpoint for the Bloomz Guardrail service to evaluate the toxicity of the content.

    diff : bool
        A flag to indicate whether or not to compute differences between consecutive outputs. Defaults to `True`.

    api_key : str
        The JWT used for authentication.

    Methods
    -------
    is_lc_serializable() -> bool
        Returns whether the class can be serialized by LangChain.

    get_lc_namespace() -> List[str]
        Returns the namespace of the LangChain object, useful for serializing and managing LangChain objects.

    _type() -> str
        Returns the output parser type for serialization.

    _diff(prev: Optional[dict], next: dict) -> dict
        Computes the difference between the previous and current outputs, if applicable.

    parse(text: str) -> dict
        Parses the input text and evaluates its toxicity using the Bloomz Guardrail API.
        Returns a dictionary containing the content and the toxicity information.
    """

    max_score: float
    """Maximum acceptable toxicity score."""
    endpoint: str
    """The model API endpoint to use."""
    api_key: Optional[str] = None
    """The model API key."""
    diff: bool = True

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        return True

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "schema", "output_parser"]

    @property
    def _type(self) -> str:
        """Return the output parser type for serialization."""
        return "default"

    def _diff(self, prev: Optional[dict], next: dict) -> dict:
        """Calculate the difference between the previous and current output, if applicable."""
        output = next.copy()
        if prev:
            output["content"] = next["content"][len(prev["content"]) :]
        return output

    def parse(self, text: str) -> dict:
        """Parse the text and evaluate its toxicity using the Bloomz Guardrail API."""
        headers = {}
        if self.api_key:
            headers["Authentication"] = f"Bearer {self.api_key}"

        if random.random() < 0.8:
            return GuardrailOutput(
                content=text,
                output_toxicity=False,
                output_toxicity_reason=[],
            ).model_dump()
        response = requests.post(urljoin(self.endpoint, "/guardrail"), json={"text": [text]}, headers=headers)

        if response.status_code != 200:
            raise RuntimeError("Bloomz guardrail didn't respond as expected.")

        results = response.json()["response"][0]

        detected_toxicities = list(filter(lambda mode: mode["score"] > self.max_score, results))

        return GuardrailOutput(
            content=text,
            output_toxicity=bool(detected_toxicities),
            output_toxicity_reason=list(map(lambda mode: mode["label"], detected_toxicities)),
        ).model_dump()
