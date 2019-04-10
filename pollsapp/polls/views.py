# python
from __future__ import unicode_literals
# libs
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# local
from .exceptions import Http400, Http404
from .models import Track, Question, Choice
from .serializers import trackSerializer, questionSerializer, choiceSerializer


def home(request):
    return HttpResponse("Hello, world. You're at the polls home.")


class trackCollection(APIView):

    def post(self, request):
        """Create a new Track"""
        serializer = trackSerializer(data=request.data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'content': serializer.data},
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        """List Tracks"""
        try:
            objs = Track.objects.all()
        except (ValueError, ValidationError):
            raise Http400(error_code='No Tracks Found.')
        totalRecords = objs.count()
        response = dict()
        response['_metadata'] = {'totalRecords': totalRecords}
        response['content'] = trackSerializer(instance=objs, many=True).data
        return Response(response)


class trackResource(APIView):

    def get(self, request, idTrack):
        """Reads a Track"""
        try:
            obj = Track.objects.get(pk=idTrack)
        except Track.DoesNotExist:
            raise Http404()
        serializer = trackSerializer(instance=obj,)
        return Response({'content': serializer.data},
                        status=status.HTTP_200_OK)

    def put(self, request, idTrack, partial=False,):
        """Update a Track"""
        try:
            obj = Track.objects.get(pk=idTrack)
        except Track.DoesNotExist:
            raise Http404()

        serializer = trackSerializer(instance=obj, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'content': serializer.data},
                        status=status.HTTP_200_OK)

    def patch(self, request, idVM):
        """Partially update a Track"""
        return self.put(request, idVM, True)

    def delete(self, request, idTrack):
        """Delete a Track"""
        try:
            obj = Track.objects.get(pk=idTrack)
        except Track.DoesNotExist:
            raise Http404()

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class questionResource(APIView):

    def get(self, request, idTrack):
        """questions based on track"""
        try:
            objs = Question.objects.filter(idTrack=idTrack)
        except (ValueError, ValidationError):
            raise Http400(error_code='No questions found on this track.')
        totalRecords = objs.count()
        response = dict()
        response['_metadata'] = {'totalRecords': totalRecords}
        response['content'] = questionSerializer(instance=objs, many=True).data
        return Response(response)
    
class choiceResource(APIView):

    def patch(self, request, idChoice):
        """Partially update a Choice"""
        try:
            obj = Choice.objects.get(pk=idChoice)
        except Choice.DoesNotExist:
            raise Http404()

        serializer = choiceSerializer(instance=obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'content': serializer.data},
                        status=status.HTTP_200_OK)


class choiceCountResource(APIView):

    def get(self, request, idQuestion):
        """Reads count of votes for a question"""
        try:
            choices=Choice.objects.select_related('idQuestion',).filter(idQuestion=idQuestion)
        except Choice.DoesNotExist:
            raise Http404()
        response = dict()
        response["choices"] = list()
        totalWrong=0
        totalCorrect=0
        for choice in choices:
            if choice.is_correct:
                totalCorrect += choice.votes
            else:
                totalWrong += choice.votes
            response["choices"].append({"choice": choice.choice, "is_correct": choice.is_correct, "votes": choice.votes})
        response["question"]=str(choice.idQuestion)
        response["totalWrongVotes"]=totalWrong
        response["totalCorrectVotes"]=totalCorrect

        return Response({'content': response},
                        status=status.HTTP_200_OK)