#!/usr/bin/python
#  -*- encoding: utf-8 -*-


from flask import Flask, render_template, request
import json
import time

app = Flask(__name__)
app.secret_key = 'masintolge_tartu'
app_default_language = 'et'

# Translators
# TODO Review this code for possible future refactoring
from parallel_translation.parallel_translation_requests import get_translations
from language.available_languages import get_available_language_culture_name_pairs, \
                                         language_culture_names_to_estonian, \
                                         language_culture_names_to_english

app.jinja_env.globals['available_language_pairs'] = get_available_language_culture_name_pairs()

app.jinja_env.globals['language_culture_names_to_estonian'] = \
    language_culture_names_to_estonian(get_available_language_culture_name_pairs())
app.jinja_env.globals['language_culture_names_to_english'] = \
            language_culture_names_to_english(get_available_language_culture_name_pairs())


@app.route('/', methods=['GET', 'POST'])
def main_page(default_language=app_default_language):
    if request.method == 'POST' and 'source_text' in request.json:
        language_translate_from = request.json['translate_from']
        language_translate_to = request.json['translate_to']
        source_text = request.json['source_text']

        print("text for translation : ", source_text)
        print("language translate from :", language_translate_from)
        print("language translate to :", language_translate_to)

        start_translation_time = time.time()
        translations = get_translations(source_text, language_translate_from, language_translate_to)
        translation_google = translations['translation_google']
        translation_microsoft = translations['translation_microsoft']
        translation_ut = translations['translation_ut']
        end_translation_time = time.time()
        print("Total translation time : ", end_translation_time - start_translation_time)

        return json.dumps({
            'status': 'OK',
            'translations': [
                {'translator': 'google', 'translation': translation_google},
                {'translator': 'ut', 'translation': translation_ut},
                {'translator': 'microsoft', 'translation': translation_microsoft}
            ]
        })

    elif request.method == 'POST':
        print(request.json)
        # TODO Create json which will return message to user
        return "OK", 201

    return render_template('index-{lang}.html'.format(lang=default_language))


@app.route('/<language>', methods=['GET'])
def get_main_page(language, default_language=app_default_language):
    try:
        return render_template('index-{lang}.html'.format(lang=language))
    except Exception as e:
        return render_template('index-{lang}.html'.format(lang=default_language))


@app.route('/about/<language>', methods=['GET'])
def about_page_estonian(language, default_language=app_default_language):
    try:
        return render_template('about-{lang}.html'.format(lang=language))
    except Exception as e:
        return render_template('about-{lang}.html'.format(lang=default_language))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
