import time

def build_meta(
    confidence=0.9,
    model_used="llama-3.3-70b",
    tokens_used=0,
    response_time_ms=0,
    cached=False,
    is_fallback=False
):
    return {
        "confidence": confidence,
        "model_used": model_used,
        "tokens_used": tokens_used,
        "response_time_ms": response_time_ms,
        "cached": cached,
        "is_fallback": is_fallback
    }