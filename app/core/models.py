from django.db import models


class Assets_Parts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    document_number = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone_number = models.CharField(max_length=255)


class Paymasters(models.Model):
    id = models.AutoField(primary_key=True)
    kind = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=255)
    email_primary = models.EmailField()
    email_secondary = models.EmailField()
    deleted_at = models.DateField(null=True,blank=True)
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)


class Authorized_Third_Parties(models.Model):
    id = models.AutoField(primary_key=True)


class Participants(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=255)
    document_number = models.CharField(max_length=255)
    authorized_third_party_id = models.ForeignKey(Authorized_Third_Parties,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    paymaster_id = models.ForeignKey(Paymasters,on_delete=models.CASCADE)


class Fk_Authorized_Third_Party_Participants(models.Model):
    authorized_third_party_id = models.ForeignKey(Authorized_Third_Parties,on_delete=models.CASCADE)
    participant_id = models.ForeignKey(Participants,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('authorized_third_party_id', 'participant_id')
        verbose_name = 'Authorized Third Party Participant'
        verbose_name_plural = 'Authorized Third Party Participants'


class Participant_Authorized_Third_Parties(models.Model):
    id = models.AutoField(primary_key=True)
    participant_id = models.ForeignKey(Participants, on_delete=models.CASCADE)
    authorized_third_party_id = models.ForeignKey(Authorized_Third_Parties,on_delete=models.CASCADE)
    deleted_at = models.DateField(null=True,blank=True)
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)
    state = models.CharField(max_length=255)
    approved_at = models.DateField(null=True)
    rejected_at = models.DateField(null=True)

class Asset_Trade_Bills(models.Model):
    id = models.AutoField(primary_key=True)
    due_date = models.DateField(null=True)
    nfe_number = models.CharField(max_length=255)
    nfe_series = models.CharField(max_length=255)
    kind = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    payer_id = models.ForeignKey(Participants,on_delete=models.CASCADE)
    endorser_original_id = models.ForeignKey(Participants,on_delete=models.CASCADE)
    new_due_date = models.DateField(null=True)
    participant_id = models.ForeignKey(Participants,on_delete=models.CASCADE)
    ballast_kind = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=255)
    payment_place = models.CharField(max_length=255)
    update_reason_kind = models.CharField(max_length=255)

