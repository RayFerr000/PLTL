from django.forms import ModelForm
from Course.models import Course


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name']