from rest_framework import serializers


class AnalyzeTextRequestSerializer(serializers.Serializer):
    text = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data


class NamedEntitySerializer(serializers.Serializer):
    persons = serializers.ListField(child=serializers.CharField())
    locations = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data


class FuzzyMatchSerializer(serializers.Serializer):
    matched = serializers.CharField()
    suggestion = serializers.CharField()
    score = serializers.FloatField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data


class FuzzyMatchesSerializer(serializers.Serializer):
    persons = FuzzyMatchSerializer(many=True)
    locations = FuzzyMatchSerializer(many=True)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data


class AnalyzeTextResponseSerializer(serializers.Serializer):
    language = serializers.CharField()
    entities = NamedEntitySerializer()
    fuzzy_matches = FuzzyMatchesSerializer()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data
