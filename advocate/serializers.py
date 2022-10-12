from rest_framework import serializers
from advocate.models import Advocate, Company, SocialLinks



class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id','url','name','logo','summary']



class SocialLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialLinks
        fields = ['name','url']

class AdvocateSerializer(serializers.ModelSerializer):
    links = SocialLinkSerializer(many=True)
    company = CompanySerializer()

    class Meta:
        model = Advocate
        fields = ['id','url','company','name','profile_pic','short_bio','long_bio','date_joined','experience','links']


class CompanyDetailSerializer(serializers.ModelSerializer):
    advocates = AdvocateSerializer(many=True)
    class Meta:
        model = Company
        fields = ['id','name','logo','advocates']