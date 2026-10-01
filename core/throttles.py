from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class GeneralUserThrottle(UserRateThrottle):
    scope = "general_user"


class GeneralAnonThrottle(AnonRateThrottle):
    scope = "general_anon"


class RecommendationThrottle(UserRateThrottle):
    scope = "recommendation"


class RecommendationAnonThrottle(AnonRateThrottle):
    scope = "recommendation_anon"