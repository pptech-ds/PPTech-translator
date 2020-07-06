import torch
import fairseq

# List available models
torch.hub.list('pytorch/fairseq')  # [..., 'transformer.wmt16.en-de', ... ]

# Load a transformer trained on WMT'16 En-De
#en2de = torch.hub.load('pytorch/fairseq', 'transformer.wmt16.en-de', tokenizer='moses', bpe='subword_nmt')

# Load a transformer trained on WMT'14 En-Fr
en2fr = torch.hub.load('pytorch/fairseq', 'transformer.wmt14.en-fr', tokenizer='moses', bpe='subword_nmt')


# The underlying model is available under the *models* attribute
assert isinstance(en2fr.models[0], fairseq.models.transformer.TransformerModel)

# Translate a sentence
print(en2fr.translate("21# 'Hallo Welt!'