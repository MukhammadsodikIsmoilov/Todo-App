from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from .models import Todo
from .serializers import TodoSerializer


class TodoAPIRoot(APIView):
    def get(self, request, format=None):
        api_urls = {
            'todos': reverse('todo:todos', request=request, format=format),
            'completed todos': reverse('todo:completed-todos', request=request, format=format),
            'active todos': reverse('todo:active-todos', request=request, format=format),
            'delete all todos': reverse('todo:delete-todos', request=request, format=format),
            'create todo': reverse('todo:create-todo', request=request, format=format),
            'todo': 'api/todos/<todo_id>',
            'update todo': 'api/todos/<todo_id>/update/',
            'delete todo': 'api/todos/<todo_id>/delete/',
        }
        return Response(api_urls)


class TodoListView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('-id')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TodoView(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class CompletedTodosView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def list(self, request, *args, **kwargs):
        todos = self.filter_queryset(self.get_queryset())
        todos = todos.filter(is_completed=True)

        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data, status=200)


class ActiveTodosView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def list(self, request, *args, **kwargs):
        todos = self.filter_queryset(self.get_queryset())
        todos = todos.filter(is_completed=False)

        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data, status=200)


class CreateTodoView(generics.CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.check_validation(self.request.data):
            self.perform_create(serializer)
            response = {
                "todo": serializer.data,
                "message": "Task created successfully"
            }
            return Response(data=response, status=201)

        return Response(data={"error": "Oops, something went wrong. Check your request data"}, status=400)

    @staticmethod
    def check_validation(data):
        return len(data['title']) > 3


class UpdateTodoView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    lookup_field = 'id'
    serializer_class = TodoSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if self.check_validation(self.request.data):
            serializer.save()
            response = {
                "todo": serializer.data,
                "message": "Task updated successfully"
            }
            return Response(data=response, status=200)

        return Response(data={"error": "Oops, something went wrong. Check your request data"}, status=400)

    @staticmethod
    def check_validation(data):
        return len(data['title']) > 3


class DeleteTodoView(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    lookup_field = 'id'
    serializer_class = TodoSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            todo = self.get_object()
            todo.delete()
            return Response(data={"message": "Task deleted successfully"}, status=200)
        finally:
            return Response(data={"error": "Oops, something went wrong. Check your request data"}, status=400)


@api_view(['DELETE'])
def deleteAllTasksView(request):
    try:
        todos = Todo.objects.all()
        todos.delete()
        return Response(data={"message": "All tasks have been deleted successfully"}, status=200)
    finally:
        return Response(data={"error": "Oops, something went wrong. Check your request data"}, status=400)
