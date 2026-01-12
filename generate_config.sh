input_directory="$1"
jq -n --arg inputDirectory "$input_directory" \
      --arg outputDirectory 'data' \
  '{$inputDirectory, $outputDirectory}' > config.json
