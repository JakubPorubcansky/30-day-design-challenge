## Replace complex function with itertools / custom iterator

Python has excellent built in libraries that can simplify many process without you having to 
re-invent the wheel every time.


## Challenge

For this challenge you need to refactor the `calculate_sensor_averages` function in the `application.py`
to use the `itertools` library functionality to perfor the exact same operation.

This operation is calculating the average value of every sensor across all devices.


## Solution (this should be sent afterwards with your explanation video (if applicable)

As you can see in the `application_itertools.py` function, we utilize the `groupby` method of `itertools`
to first group the measurements by sensor. Then the average value is calculated using the `sum` and `len` in-built
methods. Look how simpler the code is and how easier it is to read it and understand what is happening.









