# import time
#
# from inspect import isclass
# from flask import current_app, request
#
#
# def paginate(query_set, page, page_size, serializer, **kwargs):
#     count = query_set.count()
#
#     if page < 1:
#         abort(400, message="Page must be positive integer.")
#
#     if (page - 1) * page_size + 1 > count > 0:
#         abort(400, message="Page is out of range.")
#
#     if page_size > 250 or page_size < 1:
#         abort(400, message="Page size is out of range (1-250).")
#
#     results = query_set.paginate(page, page_size)
#
#     # support for old function based serializers
#     if isclass(serializer):
#         items = serializer(results.items, **kwargs).serialize()
#     else:
#         items = [serializer(result) for result in results.items]
#
#     return {"count": count, "page": page, "page_size": page_size, "results": items}
#
#
#
# def filter_by_tags(result_set, column):
#     if request.args.getlist("tags"):
#         tags = request.args.getlist("tags")
#         result_set = result_set.filter(
#             cast(column, postgresql.ARRAY(db.Text)).contains(tags)
#         )
#     return result_set
#
#
# def order_results(results, default_order, allowed_orders, fallback=True):
#     """
#     Orders the given results with the sort order as requested in the
#     "order" request query parameter or the given default order.
#     """
#     # See if a particular order has been requested
#     requested_order = request.args.get("order", "").strip()
#
#     # and if not (and no fallback is wanted) return results as is
#     if not requested_order and not fallback:
#         return results
#
#     # and if it matches a long-form for related fields, falling
#     # back to the default order
#     selected_order = allowed_orders.get(requested_order, None)
#     if selected_order is None and fallback:
#         selected_order = default_order
#     # The query may already have an ORDER BY statement attached
#     # so we clear it here and apply the selected order
#     return sort_query(results.order_by(None), selected_order)
