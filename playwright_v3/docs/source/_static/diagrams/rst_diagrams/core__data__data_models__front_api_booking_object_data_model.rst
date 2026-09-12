.. _function_class_relationships:

Function and Class Relationships
===============================

This graph shows the relationships between functions and their parent classes/modules.

.. graphviz::

    digraph G {
    node [shape=box];
    rankdir=LR;
    AdditionalNeeds [label="AdditionalNeeds"];
    Any [label="Any"];
    ApiBookingObjectPayload [label="ApiBookingObjectPayload"];
    ApiBookingObjectPayload -> from_dict;
    ApiBookingObjectPayload -> to_dict;
    BookingDates [label="BookingDates"];
    dataclass [label="dataclass"];
    field [label="field"];
}

