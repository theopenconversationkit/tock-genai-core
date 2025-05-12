# -*- coding: utf-8 -*-
"""
BloomZGuardrailSetting

Configuration settings for the BloomZ guardrail model.
This class defines the configuration required for using the BloomZ guardrail model.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal

from pydantic import Field

from tock_genai_core.models.guardrail.provider import GuardrailProvider
from tock_genai_core.models.guardrail.setting import BaseGuardrailSetting


class BloomZGuardrailSetting(BaseGuardrailSetting):
    """
    Configuration settings for the BloomZ guardrail model.
    This class defines the configuration required for using the BloomZ guardrail model.

    Attributes
    ----------

    provider: Literal[GuardrailProvider.BloomZ]
        The guardrail model provider (default: GuardrailProvider.BloomZ)
    """

    provider: Literal[GuardrailProvider.BloomZ] = Field(
        description="The guardrail model provider.", default=GuardrailProvider.BloomZ
    )
