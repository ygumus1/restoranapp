from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    ACCOUNT_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    )
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPE_CHOICES)

    def custom_signup(self, request, user):
        user.account_type = self.validated_data.get('account_type', '')
        user.save()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['account_type'] = self.validated_data.get('account_type', '')
        return data_dict
