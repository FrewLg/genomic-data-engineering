# serializers.py
class SamplesMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplesMetadata
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
