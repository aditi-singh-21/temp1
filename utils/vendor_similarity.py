from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.helper import clean_services

def similar_services(input_vendor, similar_vendors, threshold=0.3):
    vectorizer = TfidfVectorizer(stop_words='english')
    text_services = [clean_services(v.get("services", [])) for v in similar_vendors] + [clean_services(input_vendor['services'])]
    services_vectors = vectorizer.fit_transform(text_services)
    services_similarity = cosine_similarity(services_vectors[:-1], services_vectors[-1])
    text_about = [v.get("about", []) for v in similar_vendors] + [input_vendor['about']]
    about_vectors = vectorizer.fit_transform(text_about)
    about_similarity = cosine_similarity(about_vectors[:-1], about_vectors[-1])
    final_scores = (0.4* about_similarity + 0.6*services_similarity)
    summed_scores = final_scores.sum(axis=1)
    filtered_vendors = [
        (similar_vendors[i], summed_scores[i])
        for i in range(len(similar_vendors))
        if services_similarity[i] >= threshold
    ]
    
    # Rank the filtered vendors based on the combined score
    ranked_vendors = sorted(filtered_vendors, key=lambda x: x[1], reverse=True)
    return ranked_vendors