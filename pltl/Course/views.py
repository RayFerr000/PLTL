from django.shortcuts import render, render_to_response, RequestContext
from django.template import RequestContext
from Course.forms import CourseForm
from django.http import HttpResponseRedirect
from Course.models import Course


def course_list(request):
	course_info = Course.objects.all()
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			new_course = form.save(commit=False)
			new_course = form.save()
	else:
		form = CourseForm()

	return render_to_response('courses.html',{'courses': course_info, 'form': form},context_instance=RequestContext(request))

