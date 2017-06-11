class Cache:
    def __init__(self):
        self._cache = {}

    def add_page_tree(self, competitor_wca_id, competitor_page_tree):
        self._cache[competitor_wca_id] = competitor_page_tree

    def get_page_tree(self, competitor_wca_id):
        return self._cache.get(competitor_wca_id, None)
