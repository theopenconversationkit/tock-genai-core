# -*- coding: utf-8 -*-
"""
VLLMEMSetting

Configuration settings for the VLLM embedding model.
This class defines the configuration required for using the VLLM embedding model.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal
from pydantic import Field

from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.models.embedding.setting import BaseEMSetting


class VLLMEMSetting(BaseEMSetting):
    """
    Configuration settings for the VLLM embedding model.
    This class defines the configuration required for using the VLLM embedding model.

    Attributes
    ----------

    provider: Literal[EMProvider.Vllm]
        The Embedding Model provider (default: EMProvider.Vllm)
    models: str
        Model name
    """

    provider: Literal[EMProvider.Vllm] = Field(description="The Embedding Model provider.", default=EMProvider.Vllm)
    model: str = Field(description="Model name.")
