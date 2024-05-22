import os
import re

def remove_emoji(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text) # no emoji

def rename_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            # Convert filename to lowercase
            new_filename = filename.lower()
            # Remove emojis from filename
            new_filename = remove_emoji(new_filename)
            # Create full paths
            old_file = os.path.join(root, filename)
            new_file = os.path.join(root, new_filename)
            # Rename the file
            if old_file != new_file:
                os.rename(old_file, new_file)
                print(f"Renamed: {old_file} -> {new_file}")

# Example usage:
directory_path = 'Backflip_Dataset'
rename_files_in_directory(directory_path)
