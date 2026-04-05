from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class MorphosyntacticWord:
  form: str
  segmentation: str
  pos: str
  morph_tag: str
