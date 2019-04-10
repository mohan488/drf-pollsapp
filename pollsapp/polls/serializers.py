# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from . import models


class trackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = ('id', 'name', 'created', 'updated')
        read_only_fields = ('created', 'updated')

    def validate_name(self, name):
        """
        Check that value is a valid name.
        """
        if not name:
            raise serializers.ValidationError("Please enter name")
        return name


class questionSerializer(serializers.ModelSerializer):
    track = trackSerializer(read_only=True)

    class Meta: 
        model = models.Question
        fields = '__all__'
        read_only_fields = ('created', 'updated')


class choiceSerializer(serializers.ModelSerializer):
    question = questionSerializer(read_only=True)

    class Meta: 
        model = models.Choice
        fields = '__all__'
        read_only_fields = ('created', 'updated')