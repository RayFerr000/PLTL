""" assignment view"""
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import timedelta, datetime, date
from django.utils import timezone
from Course.models import Course
from Class.models import Class
from Assignment.models import Assignment
from Assignment.forms import AssignmentForm
from Assignment.PostSerializer import PostSerializer


def assignment_list(request, class_id):
    # Handle file upload
    if request.method == 'POST':
        
        req_pub_date = request.POST.get('pub_date')
        req_due_date = request.POST.get('due_date')
    
        form = AssignmentForm(request.POST, request.FILES)
        #if request.POST.get('class_id'):
        req_class_id = class_id
        #else:
        #req_class_id = 'X201'
        if form.is_valid():                  
            newdoc = Assignment(assignment_name=request.POST.get('assignment_name'), class_id=Class.objects.get(class_id=req_class_id), pub_date=req_pub_date, due_date=req_due_date, total_grade=request.POST.get('total_grade'), assignmentfile=request.FILES['assignmentfile'])
            newdoc.save()

            # Redirect to the document list after POST
        return HttpResponseRedirect(reverse('User:Class:assignment',kwargs={'class_id': req_class_id}))
    else:
        req_class_id = class_id
        form = AssignmentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Assignment.objects.all().filter(class_id=req_class_id)


    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form, 'class_id':req_class_id},context_instance=RequestContext(request))
'''

@api_view(['GET'])
def getAssignmentObject(request, pk):
    #try:
    document = Assignment.objects.filter(assignment_id=pk)
    print document
    #except document.DoesNotExist:
     #   return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(document)
        return Response(serializer)

'''

@api_view(['GET'])
def getAssignmentList(request, class_id):
 if request.method == 'GET':
  
  documents = Assignment.objects.all().filter(class_id=class_id)

  serializer = PostSerializer(documents, many=True)
  return Response(serializer.data)
