# Store application:

## Description

Simple store application

# Tables:

## User
id,
create_time,
update_time,
username,
password,
first_name,
last_name,
date_of_birth

## Product
id,
create_time,
update_time,
description,
price

## Role
id,
create_time,
update_time,
name

## Order
id,
create_time,
update_time,
user_id,
name,
status

# Requirements:
- One user can have multiple orders
- Each order can have multiple products
- Each product may exist in multiple orders
- Each user can have many roles
- Order statuses: IN_PROGRESS, FINISHED, APPROVED, DECLINED
- Roles: Client, Admin
- When order is finished, and user gets it, the price should the same when
  order was created
- Client users can
    * CRUD for orders
    * add/remove products to order
    * finish orders
    * when order is finished or approved, further change is forbidden
    * change the user info(first_name, last_name, etc.)
- Admin users can
    * CRUD users except for changing roles
    * Approve/Decline orders
    * CRUD for products
    * Get orders by status
    * Get users without orders
