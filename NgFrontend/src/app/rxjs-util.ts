import { Observable, OperatorFunction, filter, map } from 'rxjs';

export function filterDefined<T>(): OperatorFunction<T | undefined | null, T> {
  return (from: Observable<T | undefined | null>) => {
    return from.pipe(
      filter((e) => e !== undefined && e !== null),
      map((e) => e as T)
    );
  };
}
