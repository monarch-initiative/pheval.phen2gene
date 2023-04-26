from pathlib import Path

from pydantic import BaseModel, Field


class PostProcessing(BaseModel):
    score_order: str = Field(...)


class Phen2GeneToolSpecificConfigurations(BaseModel):
    environment: str = Field(...)
    phen2gene_python_executable: Path = Field(...)
    post_process: PostProcessing = Field(...)
