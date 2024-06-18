# ccrp

This library provides a basic python package to utilize Cheap Chinese Receipt Printers.

It currently only supports the "Volcora 80mm POS Thermal Receipt Printer - 50020X Series" using USB connection. [Volcora's site](https://volcora.com/products/thermal-receipt-printer?variant=39564102631479), [Amazon](https://www.amazon.com/dp/B0C1KRY98H/). There is a [User Manual](https://cdn.shopify.com/s/files/1/0257/3225/1703/files/General_User_Manual.pdf) and [Commands Manual](https://cdn.shopify.com/s/files/1/0257/3225/1703/files/Commands_Manual.pdf) online.

The receipt printer basically talks ESC/POS, but there are some minor quirks.

## Demo

You can see sample usage in `demo.py`, just run it with `python3 demo.py` or however you run your python scripts.

## Images

The printer has a system for installing bitmaps and printing them, this library implements that. You need the images in black and white binary format.
