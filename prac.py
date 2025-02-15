#Sample offsets for grid reading

sample_offsets = [
        # Center and close samples (core detection)
        (0, 0),     # Center
        (5, 0),     # Near right
        (-5, 0),    # Near left
        (0, 5),     # Near down
        (0, -5),    # Near up
        
        # Mid-distance cardinal samples (edge detection)
        (15, 0),    # Mid right
        (-15, 0),   # Mid left
        (0, 15),    # Mid down
        (0, -15),   # Mid up
        
        # Far cardinal samples (block boundary detection)
        (20, 0),    # Far right
        (-20, 0),   # Far left
        (0, 20),    # Far down
        (0, -20),   # Far up
        
        # Diagonal samples (corner detection)
        (10, 10),   # Near bottom right
        (-10, -10), # Near top left
        (-10, 10),  # Near top right
        (10, -10),  # Near bottom left
        
        # Far diagonal samples (better corner separation)
        (15, 15),   # Far bottom right
        (-15, -15), # Far top left
        (-15, 15),  # Far top right
        (15, -15),  # Far bottom left
        
        # Extra vertical confirmation (helps with vertical shapes)
        (0, 25),    # Extra far down
        (0, -25),   # Extra far up
        
        # Cross-pattern samples (helps with thin shapes)
        (7, 0),     # Close right
        (-7, 0),    # Close left
        (0, 7),     # Close down
        (0, -7),    # Close up
    ]