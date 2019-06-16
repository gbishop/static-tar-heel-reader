/* Experiment with a class to represent sets of books */

export interface BookSet {
  /* next() provides the next book id in sequence or "" when exhausted */
  next: () => string;

  /* skipTo(value) returns the next bid equal to or greater than value
   * or "" if exhausted */
  skipTo: (value: string) => string;
}

/* incrementally computes the intersection of two sets */
export class Intersection implements BookSet {
  constructor(public A: BookSet, public B: BookSet) {}

  /* a helper to advance both sequences until they match */
  align(a: string, b: string): string {
    while (a && b && a != b) {
      if (a < b) {
        a = this.A.skipTo(b);
      } else {
        b = this.B.skipTo(a);
      }
    }
    return (a && b) || '';
  }
  public next(): string {
    /* we know we can call next on both because they must have matched
     * last time */
    let a = this.A.next();
    let b = this.B.next();
    return this.align(a, b);
  }
  public skipTo(v: string): string {
    let a = this.A.skipTo(v);
    let b = this.B.skipTo(a);
    return this.align(a, b);
  }
}

/* incrementally computes the values in A that are not in B */
export class Difference implements BookSet {
  constructor(public A: BookSet, public B: BookSet) {}
  public next(): string {
    let a = this.A.next();
    let b = this.B.skipTo(a);
    while (a && b && a == b) {
      a = this.A.next();
      b = this.B.skipTo(a);
    }
    return a;
  }
  public skipTo(v: string): string {
    let a = this.A.skipTo(v);
    let b = this.B.skipTo(a);
    while (a && b && a == b) {
      a = this.A.next();
      b = this.B.skipTo(a);
    }
    return a;
  }
}

const code = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

function encode(n: number): string {
  let r = new Array(3);
  for (let i = 0; i < 3; i++) {
    r[2 - i] = code[n % 62];
    n = (n / 62) | 0;
  }
  return r.join('');
}

function decode(s: string): number {
  let r = 0;
  for (let i = 0; i < 3; i++) {
    r = r * 62 + code.indexOf(s[i]);
  }
  return r;
}

export class RangeSet implements BookSet {
  constructor(public start: string, public stop: string) {}
  current: string;
  public next(): string {
    if (!this.current) {
      this.current = this.start;
      return this.current;
    }
    this.current = encode(decode(this.current) + 1);
    if (this.current > this.stop) {
      return '';
    }
    return this.current;
  }
  public skipTo(v: string) {
    if (v < this.start) {
      v = this.start;
    }
    this.current = v;
    if (v > this.stop) {
      return '';
    }
    return v;
  }
}

export class StringSet implements BookSet {
  public index = 0;
  constructor(public values: string) {}
  public next(): string {
    this.index += 3;
    return this.values.slice(this.index, this.index + 3);
  }
  public skipTo(t: string) {
    let c,
      i = this.index,
      v = this.values;
    while ((c = v.slice(i, i + 3)) && c < t) {
      i += 3;
    }
    this.index = i;
    return c;
  }
}

export default BookSet;
