# logger
a customized console logger based on logging

python has a good library for logging; it almost meets requirements you have. But sometimes, you still want to customize something.
Basically, customized content can be specified in a yaml file; but this example is to customize programmatically.
The yaml file for conigurations has some sections that can be dynamically managed and shared. It has one customized console handler
and two console loggers:
* black-and-white
* colorful

Dependencies:
* colorama