CFG = {
    # Precise : True means no optimisations during border selection
    "precise": False,
    # Skip_step : X >= 1 (int) during distance calculation - only every Xth pixel would be taken for comparison
    "skip_step": 5,
    # Closest_count: X > 0 (int) number of the closest cells needed
    "closest_count": 10,
    # Limiting_coefficient: X > 1 (float): how many cells will be taken from priority list in relation to closest_count
    # (if closest_count = 10 and limiting_coefficient = 1.5 - for each cell 15 distances will be calculated
    "limiting_coefficient": 1.2}
