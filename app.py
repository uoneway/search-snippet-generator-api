import os
import sys
from flask import Flask, request
from flask_restx import Api, Resource
from scraper import scrap
from utils import __get_logger, gen_log_text

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMODULES_DIR = os.path.join(PROJECT_DIR, 'submodules')
sys.path.insert(0, SUBMODULES_DIR)
from summarizers.summarizers import Summarizers
import spacy
import pytextrank

logger = __get_logger()

app = Flask(__name__)
api = Api(app, version='0.01', title='Snippet Focused on Search Terms API',
        description='Make snippets focused on search terms in google search page.',
)

summ = Summarizers('normal', device='cuda')

# load a spaCy model, and add PyTextRank to the spaCy pipeline
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

@api.route('/summarize')
class Summarize(Resource):
    def post(self):
        logger.info(gen_log_text(request.json))
        data = request.json.get('data')

        src_text = scrap(data['url'])
        logger.debug(gen_log_text(src_text))

        if len(src_text) > 3000:
            doc = nlp(src_text)
            tr = doc._.textrank

            # Extractive Summarization
            extracted_sents = [str(sent) for sent in tr.summary(limit_sentences=100)]
            src_text = ' '.join(extracted_sents)
            logger.debug(gen_log_text(src_text))

        summary = summ(src_text, query=data['query'], length_penalty=1.2,)
        doc = nlp(summary)
        summary_list = [str(s).strip() for s in doc.sents if len(s) > 2]

        response = {
            'message': {
                'result': {
                    'summary_list': summary_list,
                    # 'api_rescode': 1
                }
            }
        }
        logger.info(gen_log_text(response))

        return response


if __name__ == "__main__":
    app.run(debug=True)
