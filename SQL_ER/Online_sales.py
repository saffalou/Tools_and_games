from graphviz import Digraph

# Create a top-down ER diagram
dot = Digraph(comment='Retail Media Store ER Diagram', format='png')
dot.attr(rankdir='TB', size='10')

# Define clusters and their entities
clusters = {
    'ProductMedia': {
        'label': 'Product & Media Info',
        'tables': {
            'Products': ['product_id (PK)', 'title', 'release_year', 'label_id (FK)'],
            'Editions': ['edition_id (PK)', 'product_id (FK)', 'format_id (FK)', 'barcode', 'price'],
            'Genres': ['genre_id (PK)', 'name'],
            'Formats': ['format_id (PK)', 'description'],
            'Artists': ['artist_id (PK)', 'name'],
            'ProductArtists': ['product_id (FK)', 'artist_id (FK)'],
            'ProductGenres': ['product_id (FK)', 'genre_id (FK)'],
        }
    },
    'Inventory': {
        'label': 'Inventory & Warehousing',
        'tables': {
            'Warehouses': ['warehouse_id (PK)', 'location'],
            'Stock': ['stock_id (PK)', 'edition_id (FK)', 'warehouse_id (FK)', 'quantity_available', 'incoming_quantity'],
        }
    },
    'Sales': {
        'label': 'Orders & Payments',
        'tables': {
            'Orders': ['order_id (PK)', 'customer_id (FK)', 'order_date', 'order_status'],
            'OrderItems': ['order_item_id (PK)', 'order_id (FK)', 'edition_id (FK)', 'quantity', 'preorder_expected_date'],
            'Payments': ['payment_id (PK)', 'order_id (FK)', 'amount_paid', 'payment_date', 'transaction_reference', 'is_prepayment'],
            'Refunds': ['refund_id (PK)', 'payment_id (FK)', 'amount_refunded', 'refund_date'],
            'ShippingDetails': ['shipping_id (PK)', 'order_id (FK)', 'address_id (FK)', 'shipped_date'],
        }
    },
    'Customers': {
        'label': 'Customers & Addresses',
        'tables': {
            'Customers': ['customer_id (PK)', 'name', 'email'],
            'Addresses': ['address_id (PK)', 'customer_id (FK)', 'type', 'address_line'],
        }
    }
}

# Add nodes inside clusters
for cluster_name, cluster in clusters.items():
    with dot.subgraph(name=f'cluster_{cluster_name}') as c:
        c.attr(label=cluster['label'], style='filled', color='lightgrey')
        for table, fields in cluster['tables'].items():
            label = f"{table}|{'|'.join(fields)}"
            c.node(table, shape='record', label='{' + label + '}')

# Define relationships (edges)
relationships = [
    ('Products', 'Editions'),
    ('Products', 'ProductArtists'),
    ('Products', 'ProductGenres'),
    ('Editions', 'Stock'),
    ('Formats', 'Editions'),
    ('Genres', 'ProductGenres'),
    ('Artists', 'ProductArtists'),
    ('Warehouses', 'Stock'),
    ('Customers', 'Orders'),
    ('Customers', 'Addresses'),
    ('Orders', 'OrderItems'),
    ('Orders', 'Payments'),
    ('Payments', 'Refunds'),
    ('Orders', 'ShippingDetails'),
    ('ShippingDetails', 'Addresses'),
    ('OrderItems', 'Editions')
]

# Add all relationships as edges
for src, dst in relationships:
    dot.edge(src, dst)

# Render the diagram to current directory
output_path = 'retail_media_store_er_diagram_clustered'
try:
    dot.render(output_path, format='png', cleanup=False)
    print(f"Diagram generated: {output_path}.png")
except Exception as e:
    print(f"Error rendering diagram: {e}")
