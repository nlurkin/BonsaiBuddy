import {
  Observable,
  OperatorFunction,
  UnaryFunction,
  filter,
  pipe,
} from 'rxjs';
import { CountryObject } from './types';

export function filterNullish<T>(): UnaryFunction<
  Observable<T | null | undefined>,
  Observable<T>
> {
  return pipe(
    filter((x) => x != null) as OperatorFunction<T | null | undefined, T>
  );
}

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
