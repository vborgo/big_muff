import pcbnew

board = pcbnew.GetBoard()

# Build dictionary of fixed components with their positions using field check fallback
fixed_components = {}
for fp in board.GetFootprints():
    try:
        field_value = fp.GetField("Fixed")
        if field_value == "1":
            fixed_components[fp.GetReference()] = fp.GetPosition()
    except AttributeError:
        pass  # If GetField doesn't exist or the field is missing

# Get the board edges (bounding box of the board outline)
outline_bbox = board.ComputeBoundingBox()

# Define margin from board edges (in mm)
margin_mm = 2
margin = pcbnew.FromMM(margin_mm)

# Compute placement area inside board outline
x_min = outline_bbox.GetLeft() + margin
x_max = outline_bbox.GetRight() - margin
y_min = outline_bbox.GetTop() + margin
y_max = outline_bbox.GetBottom() - margin

# Define grid spacing for placement (adjust as needed)
step_x = pcbnew.FromMM(10)
step_y = pcbnew.FromMM(10)

x = x_min
y = y_min

for fp in board.GetFootprints():
    if fp.GetReference() in fixed_components:
        continue  # Skip fixed components

    # Place component within board area
    fp.SetPosition(pcbnew.VECTOR2I(x, y))

    # Update position for next component
    x += step_x

    # If next X is outside board area, reset X and move down one row
    if x > x_max:
        x = x_min
        y += step_y

        # If Y exceeds board area, stop placement with warning
        if y > y_max:
            print("Warning: Not enough space on board to place all components.")
            break

pcbnew.Refresh()
