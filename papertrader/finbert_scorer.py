"""Score headlines with FinBERT, a free open-source model for financial sentiment.

FinBERT (ProsusAI/finbert) is a BERT model fine-tuned on financial news. It
reads a headline as a whole, so it handles cases a word list can't ("Character.AI
files for Chapter 11, puts Disney in the driver's seat" is good news for
Disney), and it costs nothing: it runs on the GitHub Actions machine, with no
account or API key. The model (about 440 MB) is downloaded from Hugging Face on
first use and cached.

The score is P(positive) - P(negative), so it lies in [-1, 1] like the other
scorers. Needs `torch` and `transformers` (see requirements-ml.txt); without
them the finbert account simply stays off.
"""

import importlib.util
import logging

log = logging.getLogger(__name__)

SCORER = "finbert"
DEFAULT_MODEL = "ProsusAI/finbert"


def available():
    return all(importlib.util.find_spec(m) is not None for m in ("torch", "transformers"))


class FinBert:
    def __init__(self, model_name=DEFAULT_MODEL, batch_size=32, max_length=64):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        labels = {i: str(l).lower() for i, l in self.model.config.id2label.items()}
        self.pos = next(i for i, l in labels.items() if l.startswith("pos"))
        self.neg = next(i for i, l in labels.items() if l.startswith("neg"))
        self.batch_size = batch_size
        self.max_length = max_length

    def predict(self, texts):
        out = []
        with self.torch.no_grad():
            for start in range(0, len(texts), self.batch_size):
                batch = texts[start:start + self.batch_size]
                enc = self.tokenizer(batch, padding=True, truncation=True, max_length=self.max_length,
                                     return_tensors="pt")
                probs = self.torch.softmax(self.model(**enc).logits, dim=-1)
                out += [float(p[self.pos] - p[self.neg]) for p in probs]
        return out


_cache = {}


def load(model_name=DEFAULT_MODEL):
    if model_name not in _cache:
        _cache[model_name] = FinBert(model_name)
    return _cache[model_name]


def score_headlines(headlines, model=None, model_name=DEFAULT_MODEL):
    """Add a "finbert" score to each headline in place. Returns the number scored.

    Raises if the model can't be loaded; the caller decides what that means.
    """
    if not headlines:
        return 0
    model = model or load(model_name)
    scores = model.predict([h.title for h in headlines])
    for h, s in zip(headlines, scores):
        h.scores[SCORER] = round(max(-1.0, min(1.0, s)), 4)
    return len(scores)
