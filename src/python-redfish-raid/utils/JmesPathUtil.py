import humanize
from jmespath import functions


class CustomFunctions(functions.Functions):
    @functions.signature({'types': ['number']})
    def _func_naturalsize(self, value):
        return humanize.naturalsize(value)

    @functions.signature({'types': ['array', 'object']}, {'types': ['']})
    def _func_fractional(self, value):
        return humanize.fractional(value)

    @functions.signature({'types': ['number']})
    def _func_scientific(self, value):
        return humanize.scientific(value)

    @functions.signature({'types': ['string']}, {'types': ['number']}, {'types': ['number']})
    def _func_substring(self, value, start_index=None, end_index=None):
        if start_index and end_index:
            start_index = max(0, int(start_index))
            end_index = min(len(value) - 1, int(end_index))
            return value[start_index:end_index]
        elif start_index:
            start_index = max(0, int(start_index))
            return value[start_index:]
        elif end_index:
            end_index = min(len(value) - 1, int(end_index))
            return value[:end_index]
        else:
            return value