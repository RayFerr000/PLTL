from rest_framework import serializers
from Assignment.models import Assignment

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ('assignment_id', 'assignment_name', \
 		 'pub_date', 'due_date', 'total_grade', 'class_id', 'assignmentfile')
