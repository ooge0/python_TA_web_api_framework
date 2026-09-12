.. _sut_description:

================================
System under test (SUT)
================================

The suite targets two practice applications built around the *restful-booker*
project.

URLs
====

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Name
     - URL
     - Purpose
   * - Back-end API
     - ``https://restful-booker.herokuapp.com``
     - Classic restful-booker.  Token auth via ``POST /auth``.  API docs at
       ``/apidoc/index.html``.
   * - Front-end API
     - ``https://automationintesting.online/api``
     - restful-booker-platform SPA backend.  Token in the body of
       ``POST /api/auth/login``.
   * - UI
     - ``https://automationintesting.online``
     - restful-booker-platform React SPA.

Both are **shared public practice services** — other users' data is visible and
mutable, and the services go to sleep or rate-limit.

Booking side
============

**Home page** (``/``).  Logo, welcome text, rooms section with room cards (type,
wheelchair option, description, amenities, "Book this room" button), contact
form, hotel contact details, map, footer with admin-panel link.

**Reservation page** (``/reservation/{id}``).  Calendar date picker, price
total, "Reserve now" button.

Admin side
==========

**Admin login** (``/#/admin``).  Username + password form; valid credentials
redirect to the rooms management view.

**Rooms** (``/#/admin``).  Table of rooms (number, type, accessible, price,
details).  Create-room form at the top; delete button per row.

**Report** (``/#/admin/report``).  Calendar view of bookings with a month
navigation toolbar.

**Branding** (``/#/admin/branding``).  B&B name, logo URL, description, map,
contact details (name, address, phone, email).

**Messages** (``/#/admin/messages``).  Inbox listing of contact-form
submissions with sender name, subject and unread badge.
