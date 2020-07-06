import json
from fairseq.models.fconv import FConvModel
from fairseq.models.transformer import TransformerModel
from modules.utils import load_model_file
from flask import Flask
from flask import request
from flask_cors import CORS
import os
import torch


# Get environment variables
HOME = os.getenv('HOME')

app = Flask(__name__)

CORS(app)

# app.config['DEBUG'] = True

MODELS_CONF = './models_conf.json'
CACHE_DIR = HOME+'/.cache/translator'

with open(MODELS_CONF) as json_file:
    models = json.load(json_file)

MODEL_EN2FR = 'en2fr_fconv_wmt14' # en2fr_fconv_wmt14 or fr2en_fconv_wmt14 or en2fr_transformer_wmt14
MODEL_EN2FR_CACHE_DIR = CACHE_DIR+'/'+MODEL_EN2FR # usually "~/.cache/<model_type>"
model_en2fr_dir = load_model_file(models[MODEL_EN2FR], MODEL_EN2FR_CACHE_DIR)
print('model_en2fr_dir: {}'.format(model_en2fr_dir))
model_fconv_en2fr = FConvModel.from_pretrained(
model_en2fr_dir,
checkpoint_file='model.pt',
tokenizer='moses', 
bpe='subword_nmt')
assert isinstance(model_fconv_en2fr.models[0], FConvModel)

#MODEL_FR2EN = 'fr2en_fconv_wmt14' # en2fr_fconv_wmt14 or fr2en_fconv_wmt14 or en2fr_transformer_wmt14
MODEL_FR2EN = 'fr2en_transformer_wmt14' # en2fr_fconv_wmt14 or fr2en_fconv_wmt14 or en2fr_transformer_wmt14
MODEL_FR2EN_CACHE_DIR = CACHE_DIR+'/'+MODEL_FR2EN # usually "~/.cache/<model_type>"
model_fr2en_dir = load_model_file(models[MODEL_FR2EN], MODEL_FR2EN_CACHE_DIR)
print('model_fr2en_dir: {}'.format(model_fr2en_dir))

# model_fconv_fr2en = FConvModel.from_pretrained(
# model_fr2en_dir,
# checkpoint_file='model.pt',
# tokenizer='moses', 
# bpe='subword_nmt')
# assert isinstance(model_fconv_fr2en.models[0], FConvModel)

model_transformer_fr2en = TransformerModel.from_pretrained(
model_fr2en_dir,
checkpoint_file='model.pt',
tokenizer='moses', 
bpe='subword_nmt')
assert isinstance(model_transformer_fr2en.models[0], TransformerModel)

# MODEL_EN2DE = 'en2de_transformer_wmt19' 
# MODEL_EN2DE_CACHE_DIR = CACHE_DIR+'/'+MODEL_EN2DE 
# model_en2de_dir = load_model_file(models[MODEL_EN2DE], MODEL_EN2DE_CACHE_DIR)
# print('model_en2de_dir: {}'.format(model_en2de_dir))
# model_transformer_en2de = TransformerModel.from_pretrained(
# model_en2de_dir,
# checkpoint_file='model.pt',
# tokenizer='moses', 
# bpe='subword_nmt')
# assert isinstance(model_en2de_dir.models[0], TransformerModel)

# MODEL_DE2EN = 'de2en_transformer_wmt19' 
# MODEL_DE2EN_CACHE_DIR = CACHE_DIR+'/'+MODEL_DE2EN 
# model_de2en_dir = load_model_file(models[MODEL_DE2EN], MODEL_DE2EN_CACHE_DIR)
# print('model_de2en_dir: {}'.format(model_de2en_dir))
# model_transformer_de2en = TransformerModel.from_pretrained(
# model_de2en_dir,
# checkpoint_file='model.pt',
# tokenizer='moses', 
# bpe='subword_nmt')
# assert isinstance(model_de2en_dir.models[0], TransformerModel)

# model_transformer_en2de = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-de', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt', tokenizer='moses', bpe='fastbpe')

# model_transformer_de2en = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.de-en', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt', tokenizer='moses', bpe='fastbpe')



@app.route('/en2fr',methods=['POST'])
def en2fr():
    txt2translate = request.form.get('text2translate')
    current_translate = model_fconv_en2fr.translate(txt2translate)
    return current_translate


@app.route('/fr2en',methods=['POST'])
def fr2en():
    txt2translate = request.form.get('text2translate')
    current_translate = model_transformer_fr2en.translate(txt2translate)
    return current_translate


# @app.route('/en2de',methods=['POST'])
# def en2de():
#     txt2translate = request.form.get('text2translate')
#     current_translate = model_transformer_en2de.translate(txt2translate)
#     return current_translate


# @app.route('/de2en',methods=['POST'])
# def de2en():
#     txt2translate = request.form.get('text2translate')
#     current_translate = model_transformer_de2en.translate(txt2translate)
#     return current_translate


# @app.route('/fr2de',methods=['POST'])
# def fr2de():
#     txt2translate = request.form.get('text2translate')
#     current_translate_fr2en = model_fconv_fr2en.translate(txt2translate)
#     current_translate_en2de = model_transformer_en2de.translate(current_translate_fr2en)
#     return current_translate_en2de


# @app.route('/de2fr',methods=['POST'])
# def de2fr():
#     txt2translate = request.form.get('text2translate')
#     current_translate_de2en = model_transformer_de2en.translate(txt2translate)
#     current_translate_en2fr = model_fconv_en2fr.translate(current_translate_de2en)
#     return current_translate_en2fr


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
