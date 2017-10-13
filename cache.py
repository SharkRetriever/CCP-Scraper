class Cache:
    def __init__(self):
        self._cache = {}

    def add_competitor_page_tree(self, competitor_wca_id, competitor_page_tree):
        self._cache[competitor_wca_id] = competitor_page_tree

    def get_competitor_page_tree(self, competitor_wca_id):
        return self._cache.get(competitor_wca_id, None)

    def add_event_results_page_tree(self, event_name, tree):
        self._cache[event_name] = tree

    def get_event_results_page_tree(self, event_name):
        return self._cache.get(event_name, None)
