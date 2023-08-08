# Car Rental System - Flask Web App


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Database Schema](#database-schema)

## Introduction

This is a Flask-based web application for a Car Rental System. The application allows users to log in with different user roles (customer, staff, and admin) and provides specific functionalities based on their roles. Customers can view available cars and manage their profiles, staff members can manage car rentals and customer profiles, while admins have full access to manage customers, staff, and cars.

## Features

- User registration and login system with password hashing and salting for secure storage.
- Role-based access control system for different user roles (customer, staff, admin).
- Customers can view available cars and their details.
- Staff can manage car rentals and customer profiles.
- Admins have full access to manage customers, staff, and cars.
- Responsive and visually appealing user interface for all dashboards.

## Technologies Used

- Python
- Flask (Micro web framework)
- MySQL (Database)
- HTML
- CSS (Bootstrap for styling)
- JavaScript
- bcrypt (Password hashing)

## Usage

1. Open the web application in your browser.
2. Register a new user account with a unique username and password.
3. Log in with the registered credentials to access the dashboard based on your role.
4. Explore the various functionalities available for customers, staff, and admins.

## Database Schema

The database schema for this project consists of the following tables:

- customers: Stores customer information and passwords.
- staff: Stores staff information and passwords.
- rental_cars: Stores information about the available rental cars.
