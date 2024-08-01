#!/bin/bash

SOURCE_DIR="/Users/temp-admin/repositories/fine_tune_llm/data/validation/archives"
BASE_DIR="/Users/temp-admin/repositories/fine_tune_llm/data/validation/raw"


# Loop through all .zip files in the source directory
for file in "$SOURCE_DIR"/*.zip; do
    # Check if file exists
    if [ -f "$file" ]; then
        # Get the base name of the file without the .zip extension
        file_name=$(basename "$file" .zip)

        # Construct the destination directory path
        dest_dir="$BASE_DIR/$file_name"

        # Create the destination directory
        mkdir -p "$dest_dir"

        # Unzip the file into the destination directory
        echo "Unzipping $file to $dest_dir"
        unzip "$file" -d "$dest_dir"
    else
        echo "No .zip files found in $SOURCE_DIR"
    fi
done
