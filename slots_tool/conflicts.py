"""Find bounded overlaps among the latest visible slot versions."""
from .core import evaluate


def detect(data, limit=100):
    if type(limit) is not int or not 1 <= limit <= 1000:
        raise ValueError('Overlap limit must be 1-1000')
    slots = evaluate(data)['slots']
    active = []
    overlaps = []
    total = 0
    for slot in slots:
        active = [prior for prior in active if prior['end'] > slot['start']]
        for prior in active:
            total += 1
            if len(overlaps) < limit:
                overlaps.append({'first': prior['id'], 'second': slot['id'],
                                 'start': slot['start'], 'end': min(prior['end'], slot['end'])})
        active.append(slot)
    return {'overlaps': overlaps, 'total': total, 'truncated': total > limit}
