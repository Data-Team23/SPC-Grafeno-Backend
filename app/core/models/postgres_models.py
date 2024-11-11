from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class AsParts(models.Model):
    id_as_parts = models.AutoField(primary_key=True)
    name_parts = models.CharField(max_length=255)
    parts_document_number = models.CharField(max_length=255)
    ct_email = models.EmailField(max_length=254, unique=True)
    ct_phone = models.CharField(max_length=255)
    deleted_at = models.DateField(null=True,blank=True)
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)
    parts_type = models.CharField(max_length=255)


class PmMasters(models.Model):
    id_masters = models.AutoField(primary_key=True)
    kind_masters = models.CharField(max_length=255)
    name_masters = models.CharField(max_length=255)
    document_masters = models.CharField(max_length=255)
    email_primary_masters = models.EmailField(max_length=254, unique=True)
    email_secondary_masters = models.EmailField(max_length=254, unique=True)
    deleted_at = models.DateField(null=True,blank=True)
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)


class PtParticipants(models.Model):
    id_participants = models.AutoField(primary_key=True)
    name_participants = models.CharField(max_length=255)
    participant_state = models.CharField(max_length=255)
    pt_ct_phone_number = models.CharField(max_length=255)
    pt_document_number = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    participants_kind = models.CharField(max_length=255)
    id_masters = models.ForeignKey(PmMasters,on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['id_masters'], name='masters_id_idx'),
        ]


class PtThirdParties(models.Model):
    id_third_parties = models.AutoField(primary_key=True)
    id_participants = models.ForeignKey(PtParticipants, on_delete=models.CASCADE)
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)
    third_parties_state = models.CharField(max_length=255)
    approved_at = models.DateField(null=True)
    rejected_at = models.DateField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['id_participants'], name='participant_id_idx'),
        ]


class ProxyThirdPartiesParticipants(models.Model):
    id_third_parties = models.ForeignKey(PtThirdParties,on_delete=models.CASCADE)
    id_participants = models.ForeignKey(PtParticipants,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_third_parties', 'id_participants')
        verbose_name = 'Authorized Third Party Participant'
        verbose_name_plural = 'Authorized Third Party Participants'
        indexes = [
            models.Index(fields=['id_third_parties'], name='px_third_party_id_idx'),
            models.Index(fields=['id_participants'], name='px_participant_id_idx'),
        ]


class AsBills(models.Model):
    id_bills = models.AutoField(primary_key=True)
    due_date = models.DateField(null=True)
    bills_nfe_number = models.CharField(max_length=255)
    bills_nfe_series = models.CharField(max_length=255)
    bills_kind = models.CharField(max_length=255)
    bills_state = models.CharField(max_length=255)
    payer_id = models.ForeignKey(PtParticipants,on_delete=models.CASCADE,related_name='payer_bills', db_column='payer_id')
    endorser_original_id = models.ForeignKey(AsParts,on_delete=models.CASCADE, related_name='endorser_bills', db_column='endorser_original_id')
    new_due_date = models.DateField(null=True)
    participant_id = models.ForeignKey(PtParticipants,on_delete=models.CASCADE)
    ballast_kind = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=255)
    payment_place = models.CharField(max_length=255)
    update_reason_kind = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['payer_id'], name='payer_id_idx'),
            models.Index(fields=['endorser_original_id'], name='endorser_original_id_idx'),
            models.Index(fields=['participant_id'], name='participant_id_idx'),
        ]