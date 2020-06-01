from django.db.models import Q


def get_stds_filters(q):
    filters = Q(first_name__icontains=q) | Q(surname__icontains=q) | Q(
        full_name__icontains=q) | Q(the_class__name__icontains=q) | Q(nid_number__exact=q)
    try:
        q = int(q)
        filters = filters | Q(id__exact=q)
    except:
        pass
    return filters
