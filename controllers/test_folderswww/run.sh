#!/bin/bash

# Install dependencies
composer install

# Run migrations
php artisan migrate

# Run database seeds
php artisan db:seed

# Start the Laravel development server
php artisan serve
