# scorer.py

def is_recognized(description: str) -> bool:

    if not description:
        return False

    text = description.lower().strip()

    rejection_phrases = [
        "i don't know",
        "unknown",
        "not sure",
        "cannot identify",
        "no information",
        "not enough information",
        "unable to determine",
    ]

    for phrase in rejection_phrases:
        if phrase in text:
            return False

    return len(description) >= 20


def model_score(description: str) -> int:
    """
    0-100
    """

    if not is_recognized(description):
        return 0

    length = len(description)

    score = 40

    score += min(length // 2, 60)

    return min(score, 100)


def calculate_strength(results):

    model_scores = {}

    recognized_models = 0

    total_score = 0

    valid_models = 0

    for model, description in results.items():

        if description.startswith("ERROR"):
            model_scores[model] = 0
            continue

        score = model_score(description)

        model_scores[model] = score

        total_score += score

        valid_models += 1

        if score > 0:
            recognized_models += 1

    avg_score = (
        total_score / valid_models
        if valid_models
        else 0
    )

    recognition_ratio = (
        recognized_models / valid_models
        if valid_models
        else 0
    )

    strength = round(
        (recognition_ratio * 700)
        + (avg_score * 3)
    )

    strength = min(strength, 1000)

    return {
        "strength": strength,
        "recognized_models": recognized_models,
        "total_models": valid_models,
        "model_scores": model_scores,
    }