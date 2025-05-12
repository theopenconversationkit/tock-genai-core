# -*- coding: utf-8 -*-
"""
BloomZEMSetting

Configuration settings for the BloomZ embedding model.
This class defines the configuration required for using the BloomZ embedding model.

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


class BloomZEMSetting(BaseEMSetting):
    """
    Configuration settings for the BloomZ embedding model.
    This class defines the configuration required for using the BloomZ embedding model.

    Attributes
    ----------

    provider: Literal[EMProvider.BloomZ]
        The Embedding Model provider (default: EMProvider.BloomZ)
    """

    provider: Literal[EMProvider.BloomZ] = Field(description="The Embedding Model provider.", default=EMProvider.BloomZ)
