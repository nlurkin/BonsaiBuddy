import {
  Observable,
  OperatorFunction,
  UnaryFunction,
  filter,
  map,
  pipe,
} from 'rxjs';

export function filterNullish<T>(): UnaryFunction<
  Observable<T | null | undefined>,
  Observable<T>
> {
  return pipe(
    filter((x) => x != null) as OperatorFunction<T | null | undefined, T>
  );
}

export function filterDefined<T>(): OperatorFunction<T | undefined | null, T> {
  return (from: Observable<T | undefined | null>) => {
    return from.pipe(
      filter((e) => e !== undefined && e !== null),
      map((e) => e as T)
    );
  };
}
