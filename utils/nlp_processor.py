import spacy

nlp = spacy.load('en_core_web_sm')
def extract_keywords(user_prompt:str):
    doc = nlp(user_prompt)
    keywords = [token.lemma.lower() for token in doc
                if not token.is_stop and not token.is_punct and token.is_alpha]
    return keywords

