import sys

import grpc

import zemberek_grpc.language_id_pb2 as z_langid
import zemberek_grpc.language_id_pb2_grpc as z_langid_g
import zemberek_grpc.normalization_pb2 as z_normalization
import zemberek_grpc.normalization_pb2_grpc as z_normalization_g
import zemberek_grpc.preprocess_pb2 as z_preprocess
import zemberek_grpc.preprocess_pb2_grpc as z_preprocess_g
import zemberek_grpc.morphology_pb2 as z_morphology
import zemberek_grpc.morphology_pb2_grpc as z_morphology_g
from django.utils.text import slugify

class MyService:
    def __init__(self):
        self.channel = grpc.insecure_channel('zemberek_container1:6789')
        self.langid_stub = z_langid_g.LanguageIdServiceStub(self.channel)
        self.normalization_stub = z_normalization_g.NormalizationServiceStub(self.channel)
        self.preprocess_stub = z_preprocess_g.PreprocessingServiceStub(self.channel)
        self.morphology_stub = z_morphology_g.MorphologyServiceStub(self.channel)

    def find_lang_id(self, i):
        response = self.langid_stub.Detect(z_langid.LanguageIdRequest(input=i))
        return response.langId

    def tokenize(self, i):
        response = self.preprocess_stub.Tokenize(z_preprocess.TokenizationRequest(input=i))
        return response.tokens

    def normalize(self, i):
        response = self.normalization_stub.Normalize(z_normalization.NormalizationRequest(input=i))
        return response

    def analyze(self, i):
        response = self.morphology_stub.AnalyzeSentence(z_morphology.SentenceAnalysisRequest(input=i))
        return response

    @staticmethod
    def fix_decode(text):
        """Pass decode."""
        if sys.version_info < (3, 0):
            return text.decode('utf-8')
        else:
            return text




