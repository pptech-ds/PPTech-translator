import torch
from fairseq.models.fconv import FConvModel
from fairseq.models.transformer import TransformerModel



model_hub_transformer_en2fr = torch.hub.load('pytorch/fairseq', 'transformer.wmt14.en-fr', tokenizer='moses', bpe='subword_nmt')

# The underlying model is available under the *models* attribute
assert isinstance(model_hub_transformer_en2fr.models[0], TransformerModel)


model_fconv_en2fr = FConvModel.from_pretrained(
    'models/wmt14.en-fr.fconv/',
    checkpoint_file='model.pt',
    tokenizer='moses', 
    bpe='subword_nmt')

assert isinstance(model_fconv_en2fr.models[0], FConvModel)


model_transformer_en2fr = TransformerModel.from_pretrained(
    'models/wmt14.en-fr.transformer/',
    checkpoint_file='model.pt',
    tokenizer='moses', 
    bpe='subword_nmt')

assert isinstance(model_transformer_en2fr.models[0], TransformerModel)


model_fconv_fr2en = FConvModel.from_pretrained(
    'models/wmt14.fr-en.fconv/',
    checkpoint_file='model.pt',
    tokenizer='moses', 
    bpe='subword_nmt')

assert isinstance(model_fconv_fr2en.models[0], FConvModel)


print('model_fconv_fr2en.translate: {}'.format(model_fconv_fr2en.translate("Bientôt des répulsifs acoustiques sur les filets pour éviter les captures accidentelles de dauphins")))
print('model_fconv_en2fr.translate: {}'.format(model_fconv_en2fr.translate("Soon acoustic repellents on nets to prevent accidental capture of dolphins")))
print('model_hub_transformer_en2fr.translate: {}'.format(model_hub_transformer_en2fr.translate("Soon acoustic repellents on nets to prevent accidental capture of dolphins")))
print('model_transformer_en2fr.translate: {}'.format(model_transformer_en2fr.translate("Soon acoustic repellents on nets to prevent accidental capture of dolphins")))





