def get_all_order_details(order):
    return {
        'underlying_symbol': get_underlying_symbol(order),
        'order_type': get_order_type(order),
        'status': get_status(order),
        'entered_time': get_entered_time(order),
        'filled_quantity': get_filled_quantity(order),
        'description': get_description(order),
        'price': get_price(order),
        'put_call': get_put_call(order),
        'instruction': get_instruction(order),
        'account_number': get_account_number(order),
        'quantity': get_quantity(order)
    }


def get_underlying_symbol(order):
    return order['orderLegCollection'][0]['instrument'].get('underlyingSymbol') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None

def get_order_type(order):
    return order['orderType']

def get_status(order):
    return order['status']

def get_entered_time(order):
    return order['enteredTime']

def get_filled_quantity(order):
    return order['filledQuantity']

def get_description(order):
    return order['orderLegCollection'][0]['instrument'].get('description') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None

def get_price(order):
    return order.get('price', None)

def get_put_call(order):
    return order['orderLegCollection'][0]['instrument'].get('putCall') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None

def get_instruction(order):
    return order['orderLegCollection'][0].get('instruction', None) if 'orderLegCollection' in order else None

def get_account_number(order):
    return order.get('accountNumber', None)

def get_quantity(order):
    return order.get('quantity', None)