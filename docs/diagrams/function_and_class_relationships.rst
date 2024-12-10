Function and Class Relationships
===============================

This graph shows the relationships between functions and their parent classes/modules. (Simple view)

.. graphviz::

    digraph G {
        node [shape=box];
        rankdir=LR;
        APIClient [label="APIClient"];
        APIClient -> _request;
        APIClient -> delete;
        APIClient -> get;
        APIClient -> patch;
        APIClient -> post;
        APIClient -> put;
        Any [label="Any"];
        dataclass [label="dataclass"];
        get_logger [label="get_logger"];
    }

