import { BonsaiEntity } from './Services/advice.service';
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

var periodIdsMap: Map<string, string> | undefined = undefined;

export function allPeriodIds(): Map<string, string> {
  if (periodIdsMap) return periodIdsMap;

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

  periodIdsMap = new Map(periods);
  return periodIdsMap;
}

export function periodIdToName(periodId: string): string | undefined {
  const periodMap = allPeriodIds();
  if (periodMap.has(periodId)) return periodMap.get(periodId);
  return periodId;
}

export function standardEntitySort(
  a: BonsaiEntity | undefined,
  b: BonsaiEntity | undefined
) {
  if (!a) return -1;
  if (!b) return 1;
  const sequenceDiff = (a.sequence ?? 99) - (b.sequence ?? 99);
  if (sequenceDiff !== 0) return sequenceDiff;
  else return (a.display_name ?? '').localeCompare(b.display_name ?? '');
}

enum Season {
  Spring = '0',
  Summer = '1',
  Autumn = '2',
  Winter = '3',
}

enum Qualifier {
  Early = '0',
  Late = '1',
  Undefined = 'Undefined', // Explicitly handle cases with no clear qualifier.
}

export function monthToPeriod(month: number): string[] {
  if (month < 1 || month > 12) {
    throw new Error('Invalid month. Month must be between 1 and 12.');
  }

  const periods: string[] = [];

  // TODO: this is applicable only to the northern hemisphere, excluding tropical regions
  if (month >= 3 && month <= 5) {
    // Spring: March-May
    periods.push(
      formatPeriod(Season.Spring, month <= 4 ? Qualifier.Early : Qualifier.Late)
    );
  }
  if (month >= 6 && month <= 8) {
    // Summer: June-August
    if (month === 6) periods.push(formatPeriod(Season.Summer, Qualifier.Early));
    else if (month === 8)
      periods.push(formatPeriod(Season.Summer, Qualifier.Late));
    else periods.push(formatPeriod(Season.Summer, Qualifier.Undefined)); // For July, explicitly marked as Undefined
  }
  if (month === 9) {
    // Early Autumn: September
    periods.push(formatPeriod(Season.Autumn, Qualifier.Early));
  }
  if (month >= 10 && month <= 11) {
    // Autumn: October-November, considering October as both Early and Late Autumn
    periods.push(
      formatPeriod(Season.Autumn, Qualifier.Early),
      formatPeriod(Season.Autumn, Qualifier.Late)
    );
  }
  if (month == 12 || month <= 2) {
    // Winter: December-February
    if (month == 12 || month == 1)
      periods.push(formatPeriod(Season.Winter, Qualifier.Early));
    if (month <= 2) periods.push(formatPeriod(Season.Winter, Qualifier.Late));
  }

  // Handle special cases explicitly if there's any month that doesn't fit well into these categories.
  return periods;
}

function formatPeriod(season: Season, qualifier: Qualifier): string {
  return `${qualifier}_${season}`;
}

export function getCurrentPeriods(): string[] {
  const curr_month = new Date().getMonth() + 1;
  return monthToPeriod(curr_month);
}
