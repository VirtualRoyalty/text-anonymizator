import os
import logging

from flask import Flask, render_template, send_from_directory

from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin

import config
from api import api, create_docs

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, EntityRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger()



configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "ru", "model_name": "ru_core_news_sm"}],
}


def create_app():
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__, template_folder='html')
    app.config.from_object('config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='AnonymizatorAPI',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0',
            securityDefinitions={
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header"
                },
            },
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
    })
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine,
                              supported_languages=["ru"])
    anonymizer = AnonymizerEngine()
    app.config['analyzer'] = analyzer
    app.config['anonymizer'] = anonymizer
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'html')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    api.init_app(app)
    app.app_context().push()

    docs = FlaskApiSpec(app)
    create_docs(docs)

    @app.route('/ping', methods=["GET"])
    def ping():
        return 'PONG.'

    @app.route('/view/<path:path>')
    def serve_static_file(path):
        if path.endswith('.html'):
            return render_template(path)
        return app.send_static_file(path)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True, reload=True)
