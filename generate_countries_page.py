"""
Generate countries.html reference page from country_codes_dic.csv
"""

import csv

# Read CSV
countries_by_region = {
    'Africa': [],
    'Europe': [],
    'North America': [],
    'South America': [],
    'Oceania': []
}

# Define regions based on country names
AFRICA_COUNTRIES = ['Cape Verde', 'Sao Tome and Principe', 'Comoros', 'Seychelles', 'Mauritius', 
                    'Madagascar', 'South Africa', 'Lesotho', 'Eswatini', 'Namibia', 'Botswana',
                    'Zimbabwe', 'Mozambique', 'Malawi', 'Zambia', 'Angola', 'Tanzania', 'Burundi',
                    'Rwanda', 'Dem. Rep. Congo', 'Kenya', 'Uganda', 'Rep. Congo', 'Gabon',
                    'Equatorial Guinea', 'Cameroon', 'Ethiopia', 'Central African Rep.', 'South Sudan',
                    'Somalia', 'Djibouti', 'Eritrea', 'Niger', 'Benin', 'Togo', 'Ivory Coast',
                    'Liberia', 'Sierra Leone', 'Guinea', 'Guinea Bissau', 'Gambia', 'Senegal',
                    'Chad', 'Mauritania', 'Burkina Faso', 'Ghana', 'Sudan', 'Mali', 'Nigeria',
                    'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Egypt']

EUROPE_COUNTRIES = ['Turkey', 'Russia', 'Romania', 'Hungary', 'Croatia', 'Bosnia and Herzegovina',
                    'Serbia', 'Kosovo', 'Albania', 'Montenegro', 'Greece', 'Moldova', 'Ukraine',
                    'Belarus', 'Lithuania', 'Finland', 'Latvia', 'Estonia', 'Sweden', 'Norway',
                    'Denmark', 'Slovenia', 'Czechia', 'Slovakia', 'Austria', 'Poland', 'Germany',
                    'Italy', 'Belgium', 'France', 'Netherlands', 'Luxembourg', 'Monaco',
                    'Liechtenstein', 'Malta', 'Vatican City', 'San Marino', 'Switzerland',
                    'Andorra', 'Spain', 'Portugal', 'United Kingdom']

NA_COUNTRIES = ['Canada', 'United States', 'Mexico', 'Costa Rica', 'El Salvador', 'Cuba',
                'St Kitts and Nevis', 'Belize', 'Haiti', 'Panama', 'Honduras', 'Guatemala',
                'Dominican Republic', 'Saint Lucia', 'Antigua and Barbuda', 'Bahamas']

SA_COUNTRIES = ['Brazil', 'Argentina', 'Venezuela', 'Colombia', 'Chile', 'Peru', 'Ecuador',
                'Paraguay', 'Uruguay', 'Guyana', 'Bolivia']

OCEANIA_COUNTRIES = ['Samoa', 'Papua New Guinea', 'Solomon Islands', 'Kiribati', 'Tonga',
                     'Fiji', 'New Zealand', 'Australia']

with open('country_codes_dic.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 2:
            continue
        country, code = row
        
        if country in AFRICA_COUNTRIES:
            countries_by_region['Africa'].append((country, code))
        elif country in EUROPE_COUNTRIES:
            countries_by_region['Europe'].append((country, code))
        elif country in NA_COUNTRIES:
            countries_by_region['North America'].append((country, code))
        elif country in SA_COUNTRIES:
            countries_by_region['South America'].append((country, code))
        elif country in OCEANIA_COUNTRIES:
            countries_by_region['Oceania'].append((country, code))

# Generate HTML
html = '''<!DOCTYPE html>
<html>
<head>
  <title>Country Codes - Grid Guessr</title>
  <style>
    body {
      background: black;
      color: white;
      font-family: sans-serif;
      padding: 20px;
    }

    .top-bar {
      width: 100%;
      text-align: left;
      padding: 5px;
      margin-bottom: 20px;
    }

    .back-btn {
      background-color: darkgray;
      color: white;
      font-size: 18px;
      padding: 10px 20px;
      border-radius: 8px;
      border: none;
      cursor: pointer;
    }

    .back-btn:hover {
      opacity: 0.9;
    }

    h1 {
      text-align: center;
      margin-bottom: 10px;
    }

    .subtitle {
      text-align: center;
      color: #888;
      margin-bottom: 40px;
    }

    .search-box {
      text-align: center;
      margin-bottom: 30px;
    }

    .search-box input {
      width: 400px;
      padding: 12px;
      font-size: 16px;
      border-radius: 8px;
      border: 1px solid #444;
      background: #222;
      color: white;
    }

    .countries-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 15px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .country-card {
      background: #1a1a1a;
      border: 1px solid #333;
      border-radius: 8px;
      padding: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .country-card:hover {
      background: #252525;
      border-color: #555;
    }

    .country-name {
      font-size: 18px;
      font-weight: 500;
    }

    .country-code {
      background: #333;
      padding: 6px 12px;
      border-radius: 6px;
      font-family: monospace;
      font-size: 16px;
      color: #0f0;
    }

    .region-header {
      grid-column: 1 / -1;
      font-size: 24px;
      font-weight: bold;
      margin-top: 30px;
      margin-bottom: 10px;
      padding-bottom: 10px;
      border-bottom: 2px solid #333;
    }

    .hidden {
      display: none;
    }
  </style>
</head>
<body>

<div class="top-bar">
  <button class="back-btn" onclick="goHome()">← Back to Home</button>
</div>

<h1>Country Code Reference</h1>
<p class="subtitle">Use these codes to specify cities in multi-country game modes</p>

<div class="search-box">
  <input type="text" id="searchInput" placeholder="Search countries..." oninput="filterCountries()">
</div>

<div class="countries-grid" id="countriesGrid">
'''

for region, countries in countries_by_region.items():
    if not countries:
        continue
    
    html += f'  <div class="region-header">{region}</div>\n'
    
    for country, code in sorted(countries):
        if code == 'N/A':
            continue
        html += f'''  <div class="country-card" data-country="{country.lower()}" data-code="{code}">
    <span class="country-name">{country}</span>
    <span class="country-code">{code}</span>
  </div>
'''

html += '''
</div>

<script>
function filterCountries() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  const cards = document.querySelectorAll('.country-card');
  
  cards.forEach(card => {
    const country = card.getAttribute('data-country');
    const code = card.getAttribute('data-code').toLowerCase();
    
    if (country.includes(searchTerm) || code.includes(searchTerm)) {
      card.classList.remove('hidden');
    } else {
      card.classList.add('hidden');
    }
  });
}

function goHome() {
  window.location.href = '/';
}
</script>

</body>
</html>
'''

with open('countries.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Generated countries.html")
