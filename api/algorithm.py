from api.models import Supplier


def retrieve_supplier(itemtypes, suppliers,
                      price_preference, distance_preference):
    """
        From the parameters, returns a sorted list of supplier_id's and
        their respective scores:
        (supplier_id, score)

        itemtypes: a list of ids that corresponding to the item types
        in the users shopping list

        suppliers: a dictionary with the key being supplier ids and the
        value being the distance from the user (in miles or minutes).
        Should only contain the suppliers near user

        price & distance preference: float between 0.00 and 9.99 based
        on user's preference for price/distance

    """
    supplier_scores = []
    avg_distance = sum(
        [dist for s, dist in suppliers.items()]) / len(suppliers)
    for supplier_id, distance in suppliers.items():
        supplier = Supplier.objects.get(id=supplier_id)
        price_score = (0.1 * float(price_preference) *
                       (sales_calculation(itemtypes, supplier) +
                        float(supplier.price_index / 5)))
        distance_score = (0.1 * float(distance_preference) *
                          min((avg_distance / distance) - 1, 1))
        supplier_scores.append((supplier_id, price_score + distance_score))
        print(distance_score)
    supplier_scores = sorted(supplier_scores, key=lambda s: s[1], reverse=True)
    return [supplier_id for supplier_id, score in supplier_scores]


def sales_calculation(itemtypes, supplier):
    """
        itemtypes: a list of ids that corresponding to the item types
        in the users shopping list

        supplier: the actual supplier model that this algorithm is judging
    """
    supplier_score = 0.0
    for item_id in itemtypes:
        sale_items = supplier.onsaleitem_set.all()
        for sale_item in sale_items:
            sale_count = 0  # counts the number of sales
            sale_track = 0.0  # tracks the sale that saves the most money
            if item_id == sale_item.item_type.id:
                sale_track = max(float(sale_item.discount), sale_track)
                sale_count += 1
            supplier_score += min(float(sale_track) +
                                  0.05 * (sale_count - 1), 1)
    return float(supplier_score)
