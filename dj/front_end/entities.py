import re
import googlesearch as GS
import spacy
from bs4 import BeautifulSoup

Nlp = spacy.load('xx_ent_wiki_sm')

class CheesySoup(BeautifulSoup):

    def get_lean_text(self):
        """Text without new lines, period after EOL."""

        txt = self.text
        lean = re.sub(r'\.?([\n\t]+ *)+', '. ', txt)

        lean = ' '.join(lean.split()) # quickly remove double spaces too

        return lean

    lean_text = property(get_lean_text)

def get_CVEs(doc: str):
    return re.findall(r'CVE-\d+-\d+', doc)

class ResultAcumulator:

    rejected_types = (
    )

    class EntityAcumulator:

        def __init__(self, name, type, url=None):
            self._name = name
            self._type = type
            self._urls = dict()

            if url:
                self.add_occurence(url)

        def get_name(self):
            return self._name
        name = property(get_name)

        def get_type(self):
            return self._type
        type = property(get_type)

        def get_urls(self):
            return self._urls.keys()
        urls = property(get_urls)

        def get_num_urls(self):
            return len(self.get_urls())
        num_urls = property(get_num_urls)

        def get_total(self):
            return sum((count for url, count in self._urls.items()))
        total = property(get_total)

        def add_occurence(self, url):
            self._urls[url] = self._urls.get(url, 0) + 1

        def iter_url_count_pairs(self):
            return ((url, count) for url, count in self._urls)


    def __init__(self):
        self.urls = set()  # processed
        self.entities = {} # entity: EntityAcumulator

    def _add_entity(self, name, type, url):
        if type in self.rejected_types: return

        if name not in self.entities:
            self.entities[name] = ResultAcumulator.EntityAcumulator(name, type)
        self.entities[name].add_occurence(url)

    def process_url(self, url: str):

        if url in self.urls:
            return

        self.urls.add(url)

        try:
            soup = CheesySoup(GS.get_page(url), 'html.parser')

            lean_text = soup.lean_text
            doc = Nlp(lean_text)

            for ent in doc.ents:
                if re.match(r'[A-Za-z0-9 -_.]{2,}', str(ent)):
                    self._add_entity(name=str(ent), type=ent.label_, url=url)

            for cve in get_CVEs(lean_text):
                self._add_entity(name=cve, type='CVE', url=url)

        except Exception as e:
            print(f'Processing "{url}" failed:\n', e)
