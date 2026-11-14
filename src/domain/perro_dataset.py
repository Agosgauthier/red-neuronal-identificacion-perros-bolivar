"""Entidad PerroDataset: una identidad del dataset con todas sus fotos."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class PerroDataset:
    id: str
    fotos: List[Path] = field(default_factory=list)
