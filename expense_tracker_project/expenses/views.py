from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Expense
from .serializers import ExpenseSerializer
from django.db.models import Sum

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = Expense.objects.filter(user=user)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user)
        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        category_breakdown = expenses.values('category').annotate(total=Sum('amount'))
        daily = expenses.values('date').annotate(total=Sum('amount'))
        monthly = {}
        for exp in expenses:
            month = exp.date.strftime('%Y-%m')
            monthly[month] = monthly.get(month, 0) + float(exp.amount)

        return Response({
            'total_expenses': total,
            'category_breakdown': category_breakdown,
            'monthly_trends': monthly,
            'daily_trends': daily,
        })
