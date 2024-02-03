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

export function periodIdToName(periodId: string): string | undefined {
  const seasons = ['Spring', 'Summer', 'Autumn', 'Winter'];
  const subsection = ['Early', 'Late'];
  const periods = seasons
    .map((season, seasonIndex) =>
      subsection.map((sub, subsectionIndex): [string, string] => [
        `${subsectionIndex}_${seasonIndex}`,
        `${sub} ${season}`,
      ])
    )
    .flat();

  const periodMap = new Map(periods);
  if (periodMap.has(periodId)) return periodMap.get(periodId);
  return periodId;
}
