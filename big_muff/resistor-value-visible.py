import pcbnew

board = pcbnew.GetBoard()

for footprint in board.GetFootprints():
    ref = footprint.GetReference()
    if ref.startswith("R"):
        for text in footprint.GraphicalItems():
            if isinstance(text, pcbnew.FOOTPRINT_TEXT) and text.GetText() == footprint.GetValue():
                text.SetVisible(True)

# Refresh the view to see changes
pcbnew.Refresh()
