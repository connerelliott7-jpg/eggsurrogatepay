// Zip code to state lookup using zip code ranges
const zipRanges = [
  { min: 35000, max: 36999, state: 'AL', name: 'Alabama' },
  { min: 99500, max: 99999, state: 'AK', name: 'Alaska' },
  { min: 85000, max: 86999, state: 'AZ', name: 'Arizona' },
  { min: 71600, max: 72999, state: 'AR', name: 'Arkansas' },
  { min: 90000, max: 96199, state: 'CA', name: 'California' },
  { min: 80000, max: 81999, state: 'CO', name: 'Colorado' },
  { min: 6000,  max: 6999,  state: 'CT', name: 'Connecticut' },
  { min: 19700, max: 19999, state: 'DE', name: 'Delaware' },
  { min: 32000, max: 34999, state: 'FL', name: 'Florida' },
  { min: 30000, max: 31999, state: 'GA', name: 'Georgia' },
  { min: 96700, max: 96899, state: 'HI', name: 'Hawaii' },
  { min: 83200, max: 83999, state: 'ID', name: 'Idaho' },
  { min: 60000, max: 62999, state: 'IL', name: 'Illinois' },
  { min: 46000, max: 47999, state: 'IN', name: 'Indiana' },
  { min: 50000, max: 52999, state: 'IA', name: 'Iowa' },
  { min: 66000, max: 67999, state: 'KS', name: 'Kansas' },
  { min: 40000, max: 42999, state: 'KY', name: 'Kentucky' },
  { min: 70000, max: 71599, state: 'LA', name: 'Louisiana' },
  { min: 3900,  max: 4999,  state: 'ME', name: 'Maine' },
  { min: 20600, max: 21999, state: 'MD', name: 'Maryland' },
  { min: 1000,  max: 2799,  state: 'MA', name: 'Massachusetts' },
  { min: 48000, max: 49999, state: 'MI', name: 'Michigan' },
  { min: 55000, max: 56799, state: 'MN', name: 'Minnesota' },
  { min: 38600, max: 39999, state: 'MS', name: 'Mississippi' },
  { min: 63000, max: 65999, state: 'MO', name: 'Missouri' },
  { min: 59000, max: 59999, state: 'MT', name: 'Montana' },
  { min: 68000, max: 69999, state: 'NE', name: 'Nebraska' },
  { min: 88900, max: 89999, state: 'NV', name: 'Nevada' },
  { min: 3000,  max: 3899,  state: 'NH', name: 'New Hampshire' },
  { min: 7000,  max: 8999,  state: 'NJ', name: 'New Jersey' },
  { min: 87000, max: 88499, state: 'NM', name: 'New Mexico' },
  { min: 10000, max: 14999, state: 'NY', name: 'New York' },
  { min: 27000, max: 28999, state: 'NC', name: 'North Carolina' },
  { min: 58000, max: 58999, state: 'ND', name: 'North Dakota' },
  { min: 43000, max: 45999, state: 'OH', name: 'Ohio' },
  { min: 73000, max: 74999, state: 'OK', name: 'Oklahoma' },
  { min: 97000, max: 97999, state: 'OR', name: 'Oregon' },
  { min: 15000, max: 19699, state: 'PA', name: 'Pennsylvania' },
  { min: 2800,  max: 2999,  state: 'RI', name: 'Rhode Island' },
  { min: 29000, max: 29999, state: 'SC', name: 'South Carolina' },
  { min: 57000, max: 57999, state: 'SD', name: 'South Dakota' },
  { min: 37000, max: 38599, state: 'TN', name: 'Tennessee' },
  { min: 75000, max: 79999, state: 'TX', name: 'Texas' },
  { min: 84000, max: 84999, state: 'UT', name: 'Utah' },
  { min: 5000,  max: 5999,  state: 'VT', name: 'Vermont' },
  { min: 20100, max: 20199, state: 'VA', name: 'Virginia' },
  { min: 22000, max: 24699, state: 'VA', name: 'Virginia' },
  { min: 98000, max: 99499, state: 'WA', name: 'Washington' },
  { min: 24700, max: 26999, state: 'WV', name: 'West Virginia' },
  { min: 53000, max: 54999, state: 'WI', name: 'Wisconsin' },
  { min: 82000, max: 83199, state: 'WY', name: 'Wyoming' },
  { min: 20000, max: 20099, state: 'DC', name: 'Washington D.C.' },
  { min: 96950, max: 96952, state: 'MP', name: 'Northern Mariana Islands' },
  { min: 96940, max: 96944, state: 'GU', name: 'Guam' },
  { min: 00600, max: 00988, state: 'PR', name: 'Puerto Rico' },
  { min: 00801, max: 00805, state: 'VI', name: 'U.S. Virgin Islands' },
];

function getStateFromZip(zip) {
  const zipStr = zip.toString().padStart(5, '0');
  const zipNum = parseInt(zipStr, 10);
  for (let range of zipRanges) {
    if (zipNum >= range.min && zipNum <= range.max) {
      return { code: range.state, name: range.name };
    }
  }
  return null;
}

function getStateTier(stateCode, serviceType) {
  // Surrogate tier 1 includes DE, egg donor does not
  const tier1Egg = ['CA', 'NY', 'MA', 'CT', 'NJ'];
  const tier1Surrogate = ['CA', 'NY', 'MA', 'CT', 'NJ', 'DE'];
  const tier2 = ['WA', 'OR', 'IL', 'TX', 'CO', 'FL', 'GA'];

  if (serviceType === 'surrogate') {
    if (tier1Surrogate.includes(stateCode)) return 'tier1';
    if (tier2.includes(stateCode)) return 'tier2';
    return 'tier3';
  } else {
    if (tier1Egg.includes(stateCode)) return 'tier1';
    if (tier2.includes(stateCode)) return 'tier2';
    return 'tier3';
  }
}

// Make available globally
window.getStateFromZip = getStateFromZip;
window.getStateTier = getStateTier;
