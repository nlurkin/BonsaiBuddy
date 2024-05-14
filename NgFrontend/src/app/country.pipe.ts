import { Pipe, PipeTransform } from '@angular/core';
import { getCountries } from './utils';
import { CountryObject } from './types';

@Pipe({
  name: 'country',
})
export class CountryPipe implements PipeTransform {
  transform(countryCode?: string): CountryObject | undefined {
    if (!countryCode) return undefined;
    return getCountries().find(
      (country) => country.countryCode === countryCode
    );
  }
}
