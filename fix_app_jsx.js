const fs = require('fs');

// Read the corrupted file
let content = fs.readFileSync('/home/ubuntu/t2india-google-homepage/src/App.jsx', 'utf8');

// Fix the corrupted line around line 372
content = content.replace(
  /}, \[searchQuery\s+const performSearch = async/,
  `}, [searchQuery])

  const performSearch = async`
);

// Write the fixed content back
fs.writeFileSync('/home/ubuntu/t2india-google-homepage/src/App.jsx', content);

console.log('Fixed App.jsx file');

