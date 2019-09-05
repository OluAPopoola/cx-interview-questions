# format of cart item is --> item = {'name':name, 'price': price, 'qty': qty)
# need a catalogue for testing
# this would normally be a lookup from a database based on some item_id

store_catalogue = [{'item_name': 'Baked Beans', 'item_price': 0.99, 'itemdiscount': 15, 'bogofdiscountstring': '2 1'},
                   {'item_name': 'Biscuits', 'item_price': 1.20, 'itemdiscount': 4, 'bogofdiscountstring': '1 1'},
                   {'item_name': 'Sardines', 'item_price': 1.89, 'itemdiscount': 10, 'bogofdiscountstring': '4 1'},
                   {'item_name': 'Shampoo (Small)', 'item_price': 2.00, 'itemdiscount': 0, 'bogofdiscountstring': '3 2'},
                   {'item_name': 'Shampoo (Medium)', 'item_price': 2.00, 'itemdiscount': 0, 'bogofdiscountstring': '2 1'},
                   {'item_name': 'Shampoo (Large)', 'item_price': 1.89, 'itemdiscount': 0, 'bogofdiscountstring': '1 1'}]


class ShoppingCart():
    def __init__(self):
        self.cart = []

    def add_item_to_cart(self, item: dict):
        if item['qty'] < 1:
            # to put an item in the cart it must have a quantity greater than 0
            raise Exception("Quantity must be greater than 0")

        print('Adding: ', item)
        if len(self.cart) == 0:
            # straight insert with no care in the world
            self.cart.append(item)
        else:
            # check to see if there is already something in the cart
            # check to see if the item is already in the basket
            for cart_item in self.cart:
                if cart_item['name'] == item['name']:
                    # already in cart so just do an update
                    self.update_cart(item['name'], item['qty'] + cart_item['qty'])
            else:
                # not already in cart
                self.cart.append(item)

    def get_shopping_cart_subtotal(self) -> float:
        return sum([item['qty']* item['price'] for item in self.cart])

    def get_shopping_cart_discount(self) -> float:
        """This function runs through the cart contents and calculates and returns the discount
             Discounts are specified in 2 ways:-
             (1) Discount as a percentage i.e 25%
             (2) Discount as buy x get 1 free
             This function should make allowance for both types
             """
        totaldiscount = 0.00
        for item in self.cart:
            # lookup whether there is a standard discount on the item
            disc = lookup_item_discount(item['name'])
            totaldiscount += (disc / 100) * item['qty'] * item['price']
        # get the second type of discount
        # This is the bogof type. For the purposes of this exercise we will assume
        # the offer is specified as a string of 2 numbers
        for item in self.cart:
            # lookup bogof offer
            offerstr = lookup_item_bogof_discount(item['name'])
            if len(offerstr) != 0:
                # means it is on an offer of some sort
                offer = offerstr.split()
                # we now have the offer
                b = int(offer[0])
                f = int(offer[1])
                if item['qty'] > (b + f):
                    # offer applies. we now need to calculate the discount to apply
                    st = int(item['qty'] / (b + f))
                    totaldiscount += (item['price'] * st * f)

        return round(totaldiscount, 2)

    def delete_item(self, name: str):
        """this function deletes the item from the cart"""
        print('Removing: {} from cart'.format(name))
        if len(self.cart) > 0:
            # something is in the cart
            for item in self.cart:
                if item['name'] == name:
                    # item exists in the cart
                    self.cart.remove(item)

    def update_cart(self, name: str, newqty: int):
        """This function updates the cart item of the given item
                it replaces the current quantity with the new one passed in"""
        print('Updating: {} quantity in cart to {}'.format(name, newqty))
        if newqty < 1:
            raise Exception("Quantity must be greater than 0")
        for item in self.cart:
            if item['name'] == name:
                # the item is in the cart
                item['qty'] = newqty

    def print_cart_contents(self):
        """Function prints out the contents of the cart -- used for debugging"""
        print("Cart's Contents\nITEM     PRICE    QUANTITY")
        for item in self.cart:
            print("{}  {:.2f}  {}".format(item['name'], item['price'], item['qty']))

    def get_cart_items_count(self) -> int :
        return sum([item['qty'] for item in self.cart])

    def print_cart_summary(self):
        self.print_cart_contents()
        cart_subtotal = self.get_shopping_cart_subtotal()
        cart_discount = self. get_shopping_cart_discount()
        print('SubTotal: £{:.2f}'.format(cart_subtotal))
        print('Discount: £{:.2f}'.format(cart_discount))
        print('Amount Due: £{:.2f}'.format(cart_subtotal - cart_discount))
        print('Item Count: {}'.format(self.get_cart_items_count()))


def get_item_dict(name: str, price: float, qty: int):
    return {'name':name, 'price': price, 'qty': qty}


def lookup_item_discount(name: str) -> int:
    """This function returns the discount associated with an item in the shops catalogue"""
    for item in store_catalogue:
        if item['item_name'] == name:
            return item['itemdiscount']


def lookup_item_bogof_discount(name: str) -> str:
    """This function returns the bogof discount string associated with the item in the shop catalog"""
    for item in store_catalogue:
        if item['item_name'] == name:
            return item['bogofdiscountstring']


def main():
    cart1 = ShoppingCart()
    item = get_item_dict('Shampoo (Small)', 2.00, 150)
    cart1.add_item_to_cart(item)
    item = get_item_dict('Shampoo (Medium)', 2.00, 50)
    cart1.add_item_to_cart(item)
    item = get_item_dict('Baked Beans', 0.99, 150)
    cart1.add_item_to_cart(item)
    item = get_item_dict('Shampoo (Large)', 1.89, 50)
    cart1.add_item_to_cart(item)
    item = get_item_dict('Biscuits', 1.20, 25)
    cart1.add_item_to_cart(item)
    cart1.delete_item('Biscuits')
    item = get_item_dict('Sardines', 1.89, 50)
    cart1.add_item_to_cart(item)
    item = get_item_dict('Shampoo (Small)', 2.00, 50)
    cart1.add_item_to_cart(item)
    cart1.print_cart_summary()


if __name__ == "__main__":
    main()
