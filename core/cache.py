from django.core.cache import cache


RECOMMENDATION_CACHE_TIMEOUT = 60 * 15  # 15 minutes


def get_recommendation_cache_key(user_id):
    return f"recommendations:user:{user_id}"


def get_cached_recommendations(user_id):
    cache_key = get_recommendation_cache_key(user_id)
    return cache.get(cache_key)


def set_cached_recommendations(user_id, data,timeout=300,):
    cache_key = get_recommendation_cache_key(user_id)

    cache.set(
        cache_key,
        data,
        timeout=RECOMMENDATION_CACHE_TIMEOUT,
    )


def delete_cached_recommendations(user_id):
    cache_key = get_recommendation_cache_key(user_id)
    cache.delete(cache_key)