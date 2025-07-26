
def sanitize_filename(name):
    # Replace invalid Windows filename characters with underscores
    invalid = r'\\/:*?"<>|'
    return ''.join('_' if c in invalid else c for c in name)
