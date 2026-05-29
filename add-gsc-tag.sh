#!/bin/bash
# Run once after getting GSC verification code from search.google.com/search-console
# Usage: bash add-gsc-tag.sh YOUR_VERIFICATION_CODE

CODE=$1
if [ -z "$CODE" ]; then
  echo "Usage: bash add-gsc-tag.sh YOUR_VERIFICATION_CODE"
  exit 1
fi

# Remove TODO placeholder comments and add real tag to all HTML files in root
for f in *.html; do
  sed -i '' "s|  <!-- TODO: Add GSC verification tag here once obtained from search.google.com/search-console -->||g" "$f"
  sed -i '' "s|  <!-- <meta name=\"google-site-verification\" content=\"PASTE_YOUR_CODE_HERE\"> -->||g" "$f"
  sed -i '' "s|<head>|<head>\n  <meta name=\"google-site-verification\" content=\"$CODE\">|" "$f"
done

# Add to all guide pages
for f in guides/*.html; do
  sed -i '' "s|<head>|<head>\n  <meta name=\"google-site-verification\" content=\"$CODE\">|" "$f"
done

echo "GSC tag added to all pages. Commit and push to deploy."
