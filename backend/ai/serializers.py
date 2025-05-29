from rest_framework import serializers
from .models import Signal, AnalyzedNews

class CamelCaseModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        new_ret = {}
        for key, value in ret.items():
            if key == 'id':
                new_ret['id'] = str(value)
            elif '_' in key:
                parts = key.split('_')
                camel = parts[0] + ''.join(word.capitalize() for word in parts[1:])
                new_ret[camel] = value
            else:
                new_ret[key] = value
        return new_ret

class SignalSerializer(CamelCaseModelSerializer):
    class Meta:
        model = Signal
        fields = '__all__'

class AnalyzedNewsSerializer(CamelCaseModelSerializer):
    class Meta:
        model = AnalyzedNews
        fields = '__all__' 