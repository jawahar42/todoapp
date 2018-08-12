from todo.models import TaskModel

from django.core.paginator import InvalidPage
from django.conf.urls import *
from django.utils import timezone
from django.http import HttpResponseBadRequest
from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie.utils import trailing_slash

class TaskModelResource(ModelResource):
    class Meta:
        queryset = TaskModel.objects.all()
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^task/search%s$" % (trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"
            ),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        search_title = request.GET.get("title", None)
        filter_due_date = request.GET.get("due", None)

        #validate search_title and due_date here

        if(search_title or filter_due_date): #apply seach filters
            search_results = TaskModel.objects.all()
            if(search_title):
                search_results = search_results.filter(title__icontains=search_title)
            if(filter_due_date):
                if(filter_due_date == 'Today'):
                    search_results = search_results.filter(due_date__day=timezone.now().day)
                elif(filter_due_date == 'ThisWeek'):
                    search_results = search_results.filter(due_date__week=timezone.now().isocalendar()[1])
                elif(filter_due_date == 'NextWeek'):
                    search_results = search_results.filter(due_date__week=(timezone.now() + timezone.timedelta(weeks=1)).isocalendar()[1])
                elif(filter_due_date == 'Overdue'):
                    search_results = search_results.filter(due_date__lte=timezone.now())
                else:
                    return  HttpResponseBadRequest('Invalid due date filter.')
        else:
            return  HttpResponseBadRequest('Invalid search request.')
        
        paginator = self._meta.paginator_class(request.GET, search_results,
            resource_uri=self.get_resource_uri(), limit=self._meta.limit,
            max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)

        to_be_serialized = paginator.page()

        bundles = [self.build_bundle(obj=result, request=request) for result in to_be_serialized['objects']]
        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        
        return self.create_response(request, to_be_serialized)