#!/bin/bash
gunicorn -b 0.0.0.0:5000 ebay_webhook:app
