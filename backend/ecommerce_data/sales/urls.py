from django.urls import path
from .views import ImportCSVView,LineChartView, BarChartView, FilterableDataTableView, SummaryMetricsView

urlpatterns = [
    path('import-csv/', ImportCSVView.as_view(), name='import-csv'),
    path("line-chart/", LineChartView.as_view(), name="line_chart"),
    path("bar-chart/", BarChartView.as_view(), name="bar_chart"),
    path("filterable-data/", FilterableDataTableView.as_view(), name="filterable_data"),
    path("summary-metrics/", SummaryMetricsView.as_view(), name="summary_metrics"),
]