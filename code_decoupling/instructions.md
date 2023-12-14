## Challenge

For this challenge you need to decouple the weather application from the code that allows it to run as cli.
In the new code it should also be possible to run the app through command line but also run the script directly
through the interpreter.

## Solution

- Bank has isinstance checks which directly couple it to different types of accounts.
- Bank is directly dependent on a specific payment service and directly sets an API key.
- Make account more generic (account type + class)
- Bank turns into functions to deposit and withdraw that get a payment service as argument
- Payment service is a protocol class, so the functions are decoupled from a specific payment service.
- The payment service object is created in the main function, and that's also where the API key is set.
- Mention single dirty place.
