from pathlib import Path

from pydantic import BaseModel, Field


class PostProcessing(BaseModel):
    """
    Postprocessing configuration.
    Attributes:
        score_order (str): The order of the results, either ascending or descending.
    """

    score_order: str = Field(...)


class Phen2GeneToolSpecificConfigurations(BaseModel):
    """
    Phen2Gene tool specific configuration options.
    Attributes:
        environment (str): The environment to run Phen2Gene tool, either local or docker.
        phen2gene_python_executable (Path): The path to the Phen2Gene python executable
        post_process (PostProcessing): The post-processing configurations.
    """

    environment: str = Field(...)
    phen2gene_python_executable: Path = Field(...)
    post_process: PostProcessing = Field(...)
