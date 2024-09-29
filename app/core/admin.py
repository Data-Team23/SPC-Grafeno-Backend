from django.contrib import admin
from core.models import (
    Log,
    Post,
    AssetsParts,
    Paymasters,
    Participants,
    ParticipantAuthorizedThirdParties,
    FkAuthorizedThirdPartyParticipants,
    AssetTradeBills
)

admin.site.register(Post)
admin.site.register(Log)
admin.site.register(AssetsParts)
admin.site.register(Paymasters)
admin.site.register(Participants)
admin.site.register(ParticipantAuthorizedThirdParties)
admin.site.register(FkAuthorizedThirdPartyParticipants)
admin.site.register(AssetTradeBills)