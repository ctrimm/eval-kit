"""Toy system under test: a rule-based classifier for 311-style messages.

Deterministic, no model, no dependencies. It is deliberately ordinary —
the point of the example is the evaluation around it, not the classifier.
Two gold cases are known misses (see example/README.md); a real system
would iterate against them only through a decision-log entry, never by
quietly editing the gold.
"""

RULES = [
    ("pothole", ["pothole", "crater", "sinkhole", "caved in", "asphalt",
                 "hole in the street", "road surface"]),
    ("streetlight", ["streetlight", "street light", "street lamp",
                     "light pole", "bulb"]),
    ("trash", ["trash", "garbage", "litter", "dumped", "dumping", "debris",
               "mattress"]),
    ("water", ["water main", "hydrant", "leaking", "leak", "pipe burst",
               "burst pipe", "flooding", "floods", "brown water",
               "storm drain", "taps"]),
    ("noise", ["loud", "amplified", "music", "jackhammer", "car alarm",
               "barking", "party"]),
    ("graffiti", ["graffiti", "spray-painted", "spray painted", "tagging",
                  "tags all over"]),
    ("parking", ["abandoned car", "abandoned vehicle", "blocking my driveway",
                 "has not moved", "hasn't moved"]),
]


def predict(case_input):
    text = " " + str(case_input).casefold() + " "
    best_label, best_score = "other", 0
    for label, keywords in RULES:
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_label, best_score = label, score
    return best_label
