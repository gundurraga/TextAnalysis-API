from gensim import corpora
from gensim.models import LdaMulticore
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)


class TopicModeler:
    def __init__(self, num_topics=5):
        self.num_topics = num_topics
        self.dictionary = None
        self.lda_model = None

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return [token for token in tokens if token not in STOPWORDS and len(token) > 3]

    def fit(self, texts):
        preprocessed_texts = [self.preprocess(text) for text in texts]
        self.dictionary = corpora.Dictionary(preprocessed_texts)
        corpus = [self.dictionary.doc2bow(text) for text in preprocessed_texts]
        self.lda_model = LdaMulticore(
            corpus=corpus, id2word=self.dictionary, num_topics=self.num_topics)

    def extract_topics(self, text):
        bow = self.dictionary.doc2bow(self.preprocess(text))
        topics = self.lda_model.get_document_topics(bow)
        return [(self.lda_model.print_topic(topic_id), score) for topic_id, score in topics]
