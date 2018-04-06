class Recommend(object):
    total = 6018832

    def __init__(self, rid, candidates):
        self.rid = rid
        self.candidates = candidates

    def get_result(self):
        keys = [key for key in self.candidates.keys() if key != self.rid]
        return sorted(keys, key=self._get_lift, reverse=True)

    def _get_lift(self, rid):
        return self._get_support_common(rid) / (self._get_support(self.rid) * self._get_support(rid))

    def _get_support(self, rid):
        return self._get_freq(rid) / self.total

    def _get_freq(self, rid):
        return self.candidates[rid]['ucount']

    def _get_support_common(self, rid):
        return self._get_freq_common(rid) / self.total

    def _get_freq_common(self, rid):
        return self.candidates[rid]['common']
