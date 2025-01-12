from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
  Store = serializers.IntegerField()
  DayOfWeek = serializers.IntegerField()
  Customers = serializers.IntegerField()
  Open = serializers.IntegerField()
  Promo = serializers.IntegerField()
  SchoolHoliday = serializers.IntegerField()
  StoreType = serializers.CharField()
  Assortment = serializers.CharField()
  CompetitionDistance = serializers.FloatField()
  CompetitionOpenSinceMonth = serializers.IntegerField()
  Promo2 = serializers.IntegerField()
  Promo2SinceWeek = serializers.IntegerField()
  Promo2SinceYear = serializers.IntegerField()
  PromoInterval = serializers.CharField()
