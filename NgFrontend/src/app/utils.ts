import { CountryObject } from './types';

const countryCodes = require('country-codes-list');
const countryCodeObject: Record<string, string> = countryCodes.customList(
  'countryCode',
  '{countryNameEn}'
);
export function getCountries(): CountryObject[] {
  return Object.keys(countryCodeObject)
    .map(
      (key): CountryObject => ({
        countryCode: key,
        countryNameEn: countryCodeObject[key],
      })
    )
    .sort((a, b) => a.countryNameEn.localeCompare(b.countryNameEn));
}
