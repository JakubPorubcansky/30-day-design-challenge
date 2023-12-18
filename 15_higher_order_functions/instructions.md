## Create high order functions

A higher-order function is a function that takes one or more functions as arguments, and/or returns a function as 
its result. In other words, a higher-order function is a function that operates on functions.

Higher-order functions are a key feature of functional programming, which is a programming paradigm that emphasizes 
the use of functions to perform computations. They enable a more declarative and expressive style of programming, 
where functions can be composed, combined, and manipulated like any other value.

Some common examples of higher-order functions in Python include map, filter, and reduce. These functions take one 
or more functions as arguments and apply them to some input data to produce a new output. 


## Challenge

For this output you need to create a higher order function based on the code of the weather application that returns
not the weather forecast itself but the functions that are able to provide us with it. 


## Solution (this should be sent afterwards with your explanation video (if applicable)

To tackle this challenge we create a new higher order function `weather_service` which returns a dictionary, whose 
values are the functions that allows us to get the weather forecast. 

Notice, how we don't need to pass the city argument
in the `weather_service` function since the `get_complete_forecast` is only defined and not called. We only pass it as
an argument later in the `run_high_order_function.py` when we call it by accessing the dictionary that the 
`weather_services` has returned.









