from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance, Vendor
from datetime import datetime, timezone


todays_date = datetime.now().date()


def get_last_valid_record(new_record, perf_qs):
    if new_record:
        last_record = perf_qs
    else:
        last_record = perf_qs.filter(date=todays_date)
    return last_record


def calculate_on_time_delivery_rate(instance, perf_qs, po_qs, new_record, expected_date) -> float:
    po_of_vendor = po_qs
    last_record = get_last_valid_record(
        new_record=new_record, perf_qs=perf_qs)
    prev_on_time_delivery_rate = last_record.latest(
        'date').on_time_delivery_rate if len(last_record) else 0
    prev_on_time_delivery_rate = 0 if not prev_on_time_delivery_rate else prev_on_time_delivery_rate
    print("DR: prev_value", prev_on_time_delivery_rate)

    total_no_orders = len(po_of_vendor)
    print("DR: total_orders", total_no_orders)
    on_time_delivered_orders = int(
        prev_on_time_delivery_rate * (total_no_orders - 1))
    print("DR: on_time_orders", on_time_delivered_orders)

    expected_delivery_date = expected_date
    actual_delivery_date = instance.delivery_date

    # expected_delivery_date = datetime(2024, 5, 17)
    # actual_delivery_date = datetime(2024, 5, 20)

    on_time_delivered_orders = on_time_delivered_orders + 1\
        if (actual_delivery_date <=
            expected_delivery_date) else on_time_delivered_orders
    print("DR: new_on_time_orders", on_time_delivered_orders)

    current_delivery_rate = round(
        on_time_delivered_orders/(total_no_orders), 2)

    return current_delivery_rate


def calculate_quality_avg_rating(instance, perf_qs, po_qs, new_record):
    completed_po_of_vendor = po_qs.filter(status="D")
    last_record = get_last_valid_record(
        new_record=new_record, perf_qs=perf_qs)
    prev_quality_rating_avg = last_record.latest(
        'date').quality_rating_avg if len(last_record) else 0
    prev_quality_rating_avg = 0 if not prev_quality_rating_avg else prev_quality_rating_avg
    total_no_completed_po = len(completed_po_of_vendor)
    sum_prev_quality_rating = prev_quality_rating_avg * total_no_completed_po
    new_sum = sum_prev_quality_rating + instance.quality_rating
    new_quality_avg = new_sum / (total_no_completed_po + 1)
    return new_quality_avg


def calculate_fullfilment_rate(instance, po_qs):
    po_qs_completed = po_qs.filter(status="D")
    total_no_of_po = len(po_qs)
    no_of_po_completed = len(po_qs_completed)
    if instance.status == "D":
        no_of_po_completed += 1

    return round(no_of_po_completed/total_no_of_po, 2)


def calculate_avg_response_time(instance, issue_date, perf_qs, po_qs, new_record):
    acknowledged_po = po_qs.filter(acknowledgment_date__isnull=False)
    no_of_ack_po = len(acknowledged_po)+1
    last_record = get_last_valid_record(
        new_record=new_record, perf_qs=perf_qs)
    prev_average_response_time = last_record.latest(
        'date').average_response_time if len(last_record) else 0
    prev_average_response_time = 0 if not prev_average_response_time else prev_average_response_time
    prev_timetaken = prev_average_response_time * (no_of_ack_po-1)
    delta = instance.acknowledgment_date.astimezone(timezone.utc) - issue_date
    current_timetaken = delta.seconds/60
    new_avg = (prev_timetaken+current_timetaken)/no_of_ack_po
    return round(new_avg, 2)


@receiver(pre_save, sender=PurchaseOrder)
def calculate_historical_performance(sender, instance, **kwargs):
    po_prev_instance = PurchaseOrder.objects.filter(
        po_number=instance.po_number)
    if po_prev_instance.exists():
        po_prev_instance_values = po_prev_instance.values()[0]
        expected_date = po_prev_instance_values['delivery_date']
        prev_status = po_prev_instance_values['status']
        prev_ack_date = po_prev_instance_values['acknowledgment_date']
        issue_date = po_prev_instance_values['issue_date']

        on_time_delivery_rate = 0
        quality_rating_avg = 0
        fullfilment_rate = 0
        avg_response_time = 0

        performance_qs = HistoricalPerformance.objects.filter(
            vendor=instance.vendor)
        po_qs = PurchaseOrder.objects.filter(vendor=instance.vendor)
        new_record = True
        new_qs = HistoricalPerformance(
            vendor=instance.vendor, date=todays_date)
        if performance_qs.filter(vendor=instance.vendor, date=todays_date).exists():
            new_record = False
            new_qs = performance_qs.get(date=todays_date)

        if prev_status != "D" and instance.status == "D":
            on_time_delivery_rate = calculate_on_time_delivery_rate(
                instance=instance, perf_qs=performance_qs, po_qs=po_qs, new_record=new_record, expected_date=expected_date)
            quality_rating_avg = calculate_quality_avg_rating(
                instance=instance, perf_qs=performance_qs, po_qs=po_qs, new_record=new_record)
            new_qs.on_time_delivery_rate = on_time_delivery_rate
            new_qs.quality_rating_avg = quality_rating_avg

        if prev_status != instance.status:
            fullfilment_rate = calculate_fullfilment_rate(
                instance=instance, po_qs=po_qs)
            new_qs.fulfillment_rate = fullfilment_rate

        if not prev_ack_date and instance.acknowledgment_date:
            avg_response_time = calculate_avg_response_time(
                instance=instance, issue_date=issue_date, perf_qs=performance_qs, po_qs=po_qs, new_record=new_record)
            new_qs.average_response_time = avg_response_time

        new_qs.save()


@receiver(post_save, sender=PurchaseOrder)
def calculate_historical_performance(sender, instance, created, **kwargs):
    kpi_qs = HistoricalPerformance.objects.filter(
        vendor=instance.vendor, date=todays_date)
    if kpi_qs.exists():
        kpi_values = kpi_qs.values()[0]
        on_time_delivery_rate = kpi_values['on_time_delivery_rate']
        quality_rating_avg = kpi_values['quality_rating_avg']
        average_response_time = kpi_values['average_response_time']
        fulfillment_rate = kpi_values['fulfillment_rate']

        vendor_qs = Vendor.objects.get(pk=instance.vendor.id)
        vendor_qs.on_time_delivery_rate = on_time_delivery_rate
        vendor_qs.quality_rating_avg = quality_rating_avg
        vendor_qs.average_response_time = average_response_time
        vendor_qs.fulfillment_rate = fulfillment_rate
        vendor_qs.save()
