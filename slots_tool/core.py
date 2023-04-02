"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value


def day(value):
    from datetime import date
    import re
    if not isinstance(value,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
        raise ValueError("Use YYYY-MM-DD")
    return date.fromisoformat(value)


def text(value,maximum=10000):
    if not isinstance(value,str) or len(value)>maximum:
        raise ValueError("Expected bounded text")
    return value

def evaluate(data):
    fields(data,("now","slots"))
    now=integer(data["now"])
    latest={}
    for row in sequence(data["slots"],1000):
        fields(row,("id","start","end","expires_at","version"))
        ident,start,end,expires,version=label(row["id"]),integer(row["start"]),integer(row["end"]),integer(row["expires_at"]),integer(row["version"],1)
        if end<=start:
            raise ValueError("Invalid slot interval")
        normalized={"id":ident,"start":start,"end":end,"expires_at":expires,"version":version}
        previous=latest.get(ident)
        if previous and previous["version"]==version and previous!=normalized:
            raise ValueError("Conflicting equal-version slot")
        if previous is None or version>previous["version"]:
            latest[ident]=normalized
    return {"slots":sorted((r for r in latest.values() if r["expires_at"]>now and r["end"]>now),key=lambda r:(r["start"],r["id"]))}
