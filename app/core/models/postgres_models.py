from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class AssetsParts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    document_number = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=254, unique=True)
    contact_phone_number = models.CharField(max_length=255)


class Paymasters(models.Model):
    id = models.AutoField(primary_key=True)
    kind = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=255)
    email_primary = models.EmailField(max_length=254, unique=True)
    email_secondary = models.EmailField(max_length=254, unique=True)
    deleted_at = models.DateField(null=True,blank=True)
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)


class Participants(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=255)
    document_number = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    paymaster_id = models.ForeignKey(Paymasters,on_delete=models.CASCADE)


class ParticipantAuthorizedThirdParties(models.Model):
    id = models.AutoField(primary_key=True)
    participant_id = models.ForeignKey(Participants, on_delete=models.CASCADE)
    authorized_third_party_id = models.CharField(max_length=255,unique=True)
    deleted_at = models.DateField(null=True,blank=True)
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)
    state = models.CharField(max_length=255)
    approved_at = models.DateField(null=True)
    rejected_at = models.DateField(null=True)


class FkAuthorizedThirdPartyParticipants(models.Model):
    authorized_third_party_id = models.ForeignKey(ParticipantAuthorizedThirdParties,on_delete=models.CASCADE)
    participant_id = models.ForeignKey(Participants,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('authorized_third_party_id', 'participant_id')
        verbose_name = 'Authorized Third Party Participant'
        verbose_name_plural = 'Authorized Third Party Participants'


class AssetTradeBills(models.Model):
    id = models.AutoField(primary_key=True)
    due_date = models.DateField(null=True)
    nfe_number = models.CharField(max_length=255)
    nfe_series = models.CharField(max_length=255)
    kind = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    payer_id = models.ForeignKey(Participants,on_delete=models.CASCADE,related_name='payer_bills', db_column='payer_id')
    endorser_original_id = models.ForeignKey(AssetsParts,on_delete=models.CASCADE, related_name='endorser_bills', db_column='endorser_original_id')
    new_due_date = models.DateField(null=True)
    participant_id = models.ForeignKey(Participants,on_delete=models.CASCADE)
    ballast_kind = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=255)
    payment_place = models.CharField(max_length=255)
    update_reason_kind = models.CharField(max_length=255)