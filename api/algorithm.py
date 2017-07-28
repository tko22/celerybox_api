from api.models import Supplier, FullPriceItem, ItemType
from django.db.models import Max


def retrieve_supplier(itemtypes, suppliers,
                      price_preference, distance_preference):
    """
        From the parameters, returns a sorted list of supplier_id from best to worst

        itemtypes: a list of ids that corresponding to the item types
        in the users shopping list

        suppliers: a dictionary with the key being supplier ids and the
        value being the distance from the user (in miles or minutes).
        Should only contain the suppliers near user

        price & distance preference: float between 0.00 and 9.99 based
        on user's preference for price/distance

        How it works:
        Currently the algorithm considers 2 preferences price and distance.
        However, it is set up in a way such that any number of preferences can be added
        and handled in the calculation.

        Each preference has a score, whose basic format is:
            preference_score = (0.1 * [preference_value] * [preference_calculation(...)]), where

            preference_value:
                a number from 0 to 10 that represents how much the user values this preference
            preference_calculation:
                a function that calculates an intermediary score for the specified supplier

            The preference_score should be a number between 0 and 1

            e.g for distance: distance_score = (0.1 * distance_preference * distance_calculation(...))

        The total supplier score is the sum of all preference scores

        Calculations:
        ------------
        Calculation Functions, like 'sales_calculation' must always:
            1. Return a calculation for a single supplier.
                Therefore, it must be a function with the supplier or an
                attribute of the supplier as a parameter
            2. Return a float between 0 and 1

        Generally, the functions' calculations follow this format:

            (Using price as an example...)
            1. Get the worst possible scenerio in the appropriate units.
                e.g getting the maximum of money that is possible to spend on the given shopping list
                ('max_total_price')
            2. Get the amount of units 'saved', relative to the worst possible scenerio, had the user went to this supplier
                e.g getting the amount of money saved from sales from a certain supplier
                ('money_saved')
            3. Return units_saved / max_units
                e.g money_saved / max_total_price
            4. (optional) Add some tie breaking mechanism
                e.g price_index

    """
    # list of (supplier_id's, scores) tuples
    supplier_scores = []

    # max_distance: cached for distance calculation
    max_distance = max([dist for s, dist in suppliers.items()])

    # for suppliers and their distances...
    for supplier_id, distance in suppliers.items():
        supplier = Supplier.objects.get(id=supplier_id)

        # price_score
        price_score = (0.1 * float(price_preference) *
                       (sales_calculation(itemtypes, supplier, suppliers.keys())))

        # distance_score
        distance_score = (0.1 * float(distance_preference) *
                          distance_calculation(distance, max_distance))

        total_score = price_score + distance_score
        supplier_scores.append((supplier_id, total_score))
    supplier_scores = sorted(supplier_scores, key=lambda s: s[1], reverse=True)
    return [supplier_id for supplier_id, score in supplier_scores]


def distance_calculation(distance, max_distance):
    """
        distance: the distance of the store whose score is being calculated

         max_distance: the distance of the farthest store in question
    """
    # get the difference in distance
    distance_saved = max_distance - distance
    # returns ratio between distance_saved and max_distance. Should always
    # return a number between 0 and 1
    return distance_saved / max_distance


def sales_calculation(itemtypes, supplier, suppliers_ids):
    """
        itemtypes: a list of ids that corresponding to the item types
        in the users shopping list

        supplier: the actual supplier model that this algorithm is judging

        suppliers_ids: a list of all supplier id's
    """
    # money_saved: total money saved from the best sales
    money_saved = 0.0

    # max_price_total: approximate maximum cost of the entire shopping list
    # across all stores. (The sum of the most expensive prices per item)
    max_price_total = 0.0

    # for each item:
    for item_id in itemtypes:

        # get all of supplier's current sales
        sale_items = supplier.onsaleitem_set.all()
        item = ItemType.objects.get(id=item_id)

        # max_price: most expensive item's price across all stores, becomes
        # None if there are no relevent FullPriceItem objects available
        max_price = FullPriceItem.objects.filter(
            item_type=item, supplier__id__in=suppliers_ids).aggregate(Max('price'))['price__max']

        # no_full_price_records: boolean that is true if max_price turn out to be None. i.e no
        # relevent FullPriceItems
        no_full_price_records = False
        if not max_price:
            # resets max_price and sets no_full_price_records to True
            no_full_price_records = True
            max_price = 0.0

        for sale_item in sale_items:
            sale_track = 0.0  # tracks the sale that saves the most money

            # In this case, since there are no full price records, the max_price will be
            # derived from the original prices of the sales.
            if no_full_price_records:
                original_price = sale_item.sale_price / sale_item.discount
                max_price = max(max_price, original_price)

            # the second condition insures that the sales_calculation stays
            # positive
            if item_id == sale_item.item_type.id and sale_item.sale_price < max_price:

                # saved_from_sale: money saved from this particular sale
                saved_from_sale = max_price - sale_item.sale_price

                # updates sale_track variable to hold the most money saved from
                # this sale
                sale_track = max(float(saved_from_sale), sale_track)

            # adds the best sale to money_saved
            money_saved += sale_track
            # adds the max_price to max_price_total
        max_price_total += max_price
    # returns the ratio of money_saved and max_price_total.
    # However, if the ratio is low enough, this calculation could also
    # return the supplier's price_index / 50. Assuming that the price_index is a number between
    # 0 and 5, the maximum (price_index/50) is 0.1 (this can be adjusted)
    # As a result, if the ratio of money_saved and max_price_total is very low for a certain
    # supplier, the sales_calculation would return the price_index/50 if it is higher.
    # This implies that a store with a very high price_index could potentially beat-out a store with more sales
    # but with low price_index.
    # should always be a value between 0 and 1. The larger the number, the
    # better the score.
    return max(float(money_saved / max_price_total), supplier.price_index / 50)
