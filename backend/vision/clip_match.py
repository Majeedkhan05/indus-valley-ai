"""
CLIP image → motif matching.
============================
Compares an uploaded seal image against:
  (a) a fixed catalogue of motif text-prompts (e.g. "an Indus unicorn seal")
  (b) optionally, the indexed seal-image embeddings from assets/seals/

Returns a ranked list of top motif matches with similarity scores.

Model: openai/clip-vit-base-patch32 (Apache 2.0, ~600 MB).
Override with env var IVAI_CLIP_MODEL.
"""
from __future__ import annotations

import io
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional

import numpy as np
from PIL import Image

log = logging.getLogger("ivai.clip")

CLIP_MODEL_NAME = os.environ.get("IVAI_CLIP_MODEL", "openai/clip-vit-base-patch32")

# Reference motif catalogue — text prompts that CLIP has been trained
# to associate with these visual concepts.
MOTIF_CATALOGUE = [
    ("unicorn",          "a square Indus Valley steatite seal showing a one-horned unicorn-like bull in profile with a manger or standard"),
    ("zebu bull",        "an Indus Valley seal depicting a humped zebu bull"),
    ("elephant",         "an Indus seal with a side-profile elephant"),
    ("tiger",            "an Indus seal showing a tiger or large feline"),
    ("rhinoceros",       "an Indus seal showing a rhinoceros"),
    ("water buffalo",    "an Indus seal showing a water buffalo with curved horns"),
    ("composite animal", "an Indus seal showing a composite or hybrid mythological creature"),
    ("seated yogic figure (Pashupati)", "the Pashupati seal — a seated horned figure surrounded by animals"),
    ("pipal tree",       "an Indus seal depicting a sacred pipal tree"),
    ("script-only tablet","a small rectangular Indus tablet with only inscribed signs and no animal motif"),
    ("inscription / sign sequence", "a row of Indus script signs, line drawing or carved inscription"),
    ("fish sign",        "the Indus 'fish' sign — a stylised fish glyph from the script"),
    ("jar sign",         "the Indus 'jar' sign — a U-shaped or pot-like glyph used as a suffix"),
    ("worship scene",    "an Indus seal showing humans, animals, and deities in a worship or ritual scene"),
    ("dancing girl figurine", "a small bronze figurine of a standing female with bangles, the 'Dancing Girl'"),
    ("priest-king statuette", "a small stone bust of a bearded man with a fillet — the 'Priest-King'"),
    ("mother goddess figurine", "a Harappan terracotta female figurine with elaborate headdress"),
    ("city plan or aerial photograph", "an aerial view or site plan of an excavated Indus city"),
    ("brick architecture", "Indus mud-brick or fired-brick architectural ruins"),
]


class CLIPMatcher:
    def __init__(self, model_name: str = CLIP_MODEL_NAME):
        from transformers import CLIPProcessor, CLIPModel
        import torch
        log.info(f"Loading CLIP: {model_name}")
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        self.model = CLIPModel.from_pretrained(model_name).to(self.device).eval()
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.text_features = self._embed_motif_catalogue()
        log.info(f"  CLIP ready on {self.device} — catalogue size: {len(MOTIF_CATALOGUE)}")

    def _embed_motif_catalogue(self) -> np.ndarray:
        import torch
        prompts = [p for _, p in MOTIF_CATALOGUE]
        inputs = self.processor(text=prompts, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            feats = self.model.get_text_features(**inputs)
            feats = feats / feats.norm(dim=-1, keepdim=True)
        return feats.cpu().numpy()

    def _embed_image_bytes(self, raw: bytes) -> np.ndarray:
        import torch
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        inputs = self.processor(images=img, return_tensors="pt").to(self.device)
        with torch.no_grad():
            feats = self.model.get_image_features(**inputs)
            feats = feats / feats.norm(dim=-1, keepdim=True)
        return feats.cpu().numpy().squeeze()

    def match_motif(self, raw: bytes, top_k: int = 5) -> List[Dict]:
        img_vec = self._embed_image_bytes(raw)               # (D,)
        sims = self.text_features @ img_vec                  # cosine — (N,)
        idx = np.argsort(-sims)[:top_k]
        return [
            {
                "motif":      MOTIF_CATALOGUE[i][0],
                "prompt":     MOTIF_CATALOGUE[i][1],
                "similarity": float(sims[i]),
            }
            for i in idx
        ]

    def embed_known_seals(self, seals_dir: Path) -> Optional[np.ndarray]:
        """Optional: pre-embed the assets/seals/ folder for image-image matching."""
        if not seals_dir.exists():
            return None
        files = sorted(seals_dir.glob("*.jpg"))
        if not files:
            return None
        vecs = []
        for f in files:
            with f.open("rb") as fh:
                vecs.append(self._embed_image_bytes(fh.read()))
        return np.stack(vecs)
