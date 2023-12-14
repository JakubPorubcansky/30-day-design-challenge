## Add configuration file to store all external parameters 

A configuration file allows you to store settings or parameters separately from the code. This makes it easier to 
modify or manage these settings without changing the code itself, and also allows you to use the same code with 
different configurations, easier than when you need to find that value in the code itself.


## Challenge

For this challenge you need to modify the weather app to parse (and compose) the parameters it needs for successfully 
calling the `OpenWeatherMap` api. By the end of the challenge, when you need to run for another city or using a 
different api key, you should only modify the configuration file.


## Solution (this should be sent afterwards with your explanation video (if applicable)

In the modified file `app_with_config_file.py` you can see that we added an extra parameter in the constructor of the 
`WeatherApi` called `config` which is a dictionary with the configuration parameters that we defined in the 
`config.json` file.

The constructor uses this dictionary to initialize/parse the parameters `api_key`, `city` and `url_pattern` as 
object attributes. Then the `get_complete_forecast` function composes the correct url. Notice doesn't need any external 
parameters anymore (`city`), as this is already known from the constructor.

Notice, how after modifying the code to work with a config file, the user interface becomes simpler, since you only
need to modify a json file and flatter, since all arguments are passed at the same level, while before `api_key` and 
`city` where passed at different levels, while the `url` was hardcoded, making it more difficult to change it in case
the service was changed or updated. 

We could also modify the code to give the print statements that are now defined in the `run.py` directly in the app code,
either on the `WeatherApi` function members or in the `WeatherService` function members. This would also become easier
now that we have the config file. You can try that if you want :-)









