from typing import Iterable, Optional, Union

from embedchain.config import BaseLlmConfig
from embedchain.helper.json_serializable import register_deserializable
from embedchain.llm.base import BaseLlm


@register_deserializable
class GPT4AllLlm(BaseLlm):
    DEFAULT_MODEL = "orca-mini-3b.ggmlv3.q4_0.bin"

    def __init__(self, config: Optional[BaseLlmConfig] = None):
        super().__init__(config=config)
        if self.config.model is None:
            self.config.model = GPT4AllLlm.DEFAULT_MODEL
        self.instance = GPT4AllLlm._get_instance(self.config.model)

    def repair(self):
        """
        Repair object after deserialization.
        """
        # This method exists because embedchain can only serialize attributes,
        # and only those that are part of it.
        # This method regenerates the non-serializable parts from the serialized config.
        repaired = False
        if not hasattr(self.config, "model") or self.config.model is None:
            self.config.model = GPT4AllLlm.DEFAULT_MODEL
            repaired = True
        if not hasattr(self, "instance"):
            self.instance = GPT4AllLlm._get_instance(self.config.model)
            repaired = True
        return repaired

    def get_llm_model_answer(self, prompt):
        return self._get_gpt4all_answer(prompt=prompt, config=self.config)

    @staticmethod
    def _get_instance(model):
        try:
            from gpt4all import GPT4All
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "The GPT4All python package is not installed. Please install it with `pip install --upgrade embedchain[opensource]`"  # noqa E501
            ) from None

        return GPT4All(model_name=model or GPT4AllLlm.DEFAULT_MODEL)

    def _get_gpt4all_answer(self, prompt: str, config: BaseLlmConfig) -> Union[str, Iterable]:
        if config.model and config.model != self.config.model:
            raise RuntimeError(
                "OpenSourceApp does not support switching models at runtime. Please create a new app instance."
            )

        if config.system_prompt:
            raise ValueError("OpenSourceApp does not support `system_prompt`")

        response = self.instance.generate(
            prompt=prompt,
            streaming=config.stream,
            top_p=config.top_p,
            max_tokens=config.max_tokens,
            temp=config.temperature,
        )
        return response
