API client class representation
=================================

**Fancy graphviz API client class representation**

.. graphviz::

    digraph G {
        label="API Client Function Relationships";
        fontsize=20;
        labelloc=top;
        fontname="Helvetica";

        // Define the style for all nodes
        node [shape=box, style=filled, color=lightblue2, fontname="Arial", fontsize=12];

        // Define the style for edges
        edge [color=darkgreen, style=dashed, penwidth=1.5];

        // APIClient node with 3D box style
        "APIClient" [label="APIClient", shape=box3d, color=lightblue];

        // Edges from APIClient to its methods
        "APIClient" -> "_request" [label="uses", color="blue", fontcolor="blue", fontsize=10];
        "APIClient" -> "delete" [label="calls", color="red", fontcolor="red", fontsize=10, style="solid"];
        "APIClient" -> "get" [label="calls", color="purple", fontcolor="purple", fontsize=10, style="solid"];
        "APIClient" -> "patch" [label="calls", color="orange", fontcolor="orange", fontsize=10, style="dashed"];
        "APIClient" -> "post" [label="calls", color="green", fontcolor="green", fontsize=10, style="solid"];
        "APIClient" -> "put" [label="calls", color="brown", fontcolor="brown", fontsize=10, style="solid"];

        // Additional nodes
        "Any" [label="Any", shape=ellipse, color=yellow];
        "dataclass" [label="dataclass", shape=ellipse, color=palegreen];
        "get_logger" [label="get_logger", shape=ellipse, color=lightcoral];

        // Define relationships to external dependencies
        "APIClient" -> "Any" [style=dotted];
        "APIClient" -> "dataclass" [style=dashed, color="gray"];
        "APIClient" -> "get_logger" [style=dashed, color="gray"];
    }