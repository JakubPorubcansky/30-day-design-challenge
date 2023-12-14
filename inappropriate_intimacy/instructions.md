## Add functionality for shopping cart to support multiple discounts and combine them


## Challenge

For this challenge you need to tweak the shopping cart app to allow for different types of discounts, or combinations 
of discounts.


## Solution (this should be sent afterwards with your explanation video (if applicable)

To add the functionality we can create a new attribute in the `ShoppingCart` class to store the different kind of 
discounts with their respective values. This can be a list of dictinaries where each dictionary represents a discount.
Each discount can have a `type` and a `value`, where the `type` can be a `voucher` or a `percentage` and the value can 
be the voucher code or the percentage value respectively.

We then need to tweak the `compute_total` and `print_cart` functions to look for those discounts and handle them 
appropriately. That is to apply them for the first and to print them for the second.










