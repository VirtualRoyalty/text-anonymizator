from flask import jsonify, current_app, request, render_template
from flask_restful import Resource, reqparse

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields


class TestResponseSchema(Schema):
    message = fields.Str(example="Success")


class TestResource(Resource, MethodResource):
    @doc(summary='Test Resourse', tags=['Test'])
    @marshal_with(TestResponseSchema)
    def get(self, test_str):
        return jsonify({'message': test_str})


class AnonRequestSchema(Schema):
    text = fields.String(required=True, default="""
                Здравствуйте, меня зовут Дэвид Джонсон, и я живу в штате Мэн.
                Номер моей кредитной карты - 4095-2609-9393-4932, а идентификатор моего криптокошелька - 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ.
                18 сентября я посетил сайт microsoft.com и отправил письмо на адрес test@presidio.site с IP 192.168.0.1."""
                         )


class TextAnonymizatorResource(Resource, MethodResource):
    parser = reqparse.RequestParser()
    parser.add_argument('text', type=str, required=True, help='This field cannot be left blank')

    @doc(summary='Text anonymizator Resourse', tags=['Anonymize'])
    @use_kwargs(AnonRequestSchema, location=('querystring'))
    def get(self, **kwargs):
        text = request.args.get("text", type=str)
        analyzer = current_app.config['analyzer']
        anonymizer = current_app.config['anonymizer']
        anon_text = anonymize_text(text, analyzer, anonymizer)
        return jsonify({'text': text,
                        'anonymized_text': anon_text})


class HTMLAnonRequestSchema(Schema):
    url = fields.String(required=True, default="""https://ria.ru/20211102/kino-1757235169.html""")


class HTMLAnonymizatorResource(Resource, MethodResource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help='This field cannot be left blank')

    @doc(summary='HTML anonymizator Resourse', tags=['Anonymize'])
    @use_kwargs(HTMLAnonRequestSchema, location=('querystring'))
    def get(self, **kwargs):
        url = request.args.get("url", type=str)
        analyzer = current_app.config['analyzer']
        anonymizer = current_app.config['anonymizer']
        _folder = current_app.config['UPLOAD_FOLDER']
        soup = get_html(url)
        anon_html = anonymize_html(soup, analyzer, anonymizer, operators, _folder)
        return jsonify({'url': "http://192.168.99.100:5000/view/test.html"})


def anonymize_text(text, analyzer, anonymizer, language='ru', operators=None):
    results = analyzer.analyze(text, language=language)
    anon_text = anonymizer.anonymize(text,
                                     analyzer_results=results,
                                     operators=operators)
    return anon_text.text


from presidio_anonymizer.entities.engine import OperatorConfig
from bs4 import BeautifulSoup, NavigableString
import requests


def get_box(text, color='green'):
    return f"[{text}]"


operators = {"PERSON": OperatorConfig(operator_name="replace",
                                      params={"new_value": get_box('PERSON', 'green')}),
             "LOCATION": OperatorConfig(operator_name="replace",
                                        params={"new_value": get_box('LOC', 'orange')}),
             "ORGANIZATION": OperatorConfig(operator_name="replace",
                                            params={"new_value": get_box('ORG', 'red')}),
             "ORG": OperatorConfig(operator_name="replace",
                                   params={"new_value": get_box('ORG', 'red')}),
             }


def get_html(url="https://ria.ru/20211102/kino-1757235169.html"):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    for x in soup.find_all('a'):
        new_tag = soup.new_tag('a')
        if x.string:
            new_tag = x.string
        x.replace_with(new_tag)
    return soup


def anonymize_html_object(html_obj, analyzer, anonymizer, operators, *args):
    for x in list(html_obj.strings):
        anon_text = anonymize_text(str(x), analyzer, anonymizer, operators=operators)
        x.replaceWith(anon_text)
    return None


def anonymize_html(soup, analyzer, anonymizer, operators, folder):
    title = soup.find(attrs={'class': 'article__title'})
    second_title = soup.find(attrs={'class': 'article__second-title'})
    body = soup.find_all('div', attrs={'class': 'article__text'})
    try:
        html_content = anonymize_html_object(title, analyzer, anonymizer, operators)
    except Exception as e:
        print(e)
    try:
        html_content = anonymize_html_object(second_title, analyzer, anonymizer, operators)
    except Exception as e:
        print(e)
    for content in body:
        html_content = anonymize_html_object(content, analyzer, anonymizer, operators)
    filepath = folder + "/test.html"
    with open(filepath, "w", encoding='utf8') as f:
        f.write(str(soup))
    return filepath
