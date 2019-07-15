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

export class Limit implements BookSet {
  constructor(public A: BookSet, public limit: string) {}
  public next(): string {
    const r = this.A.next();
    return r <= this.limit ? r : "";
  }
  public skipTo(v: string): string {
    const r = this.A.skipTo(v);
    return r <= this.limit ? r : "";
  }
}

const code = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

export class RangeSet implements BookSet {
  constructor(
    public start: string,
    public stop: string,
    public digits: number,
    public base: number,
  ) {}
  current: string;
  public next(): string {
    if (!this.current) {
      this.current = this.start;
      return this.current;
    }
    this.current = this.encode(this.decode(this.current) + 1);
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
  encode(n: number): string {
    let r = new Array(this.digits);
    for (let i = 0; i < this.digits; i++) {
      r[2 - i] = code[n % this.base];
      n = (n / this.base) | 0;
    }
    return r.join('');
  }

  decode(s: string): number {
    let r = 0;
    for (let i = 0; i < this.digits; i++) {
      r = r * this.base + code.indexOf(s[i]);
    }
    return r;
  }
}

export class StringSet implements BookSet {
  public index: number;
  constructor(public values: string, public digits: number) {
    this.index = -digits;
  }
  public next(): string {
    this.index += this.digits;
    return this.values.slice(this.index, this.index + this.digits);
  }
  public skipTo(t: string) {
    let c,
      i = Math.max(0, this.index),
      v = this.values,
      d = this.digits;
    while ((c = v.slice(i, i + d)) && c < t) {
      i += d;
    }
    this.index = i;
    return c;
  }
}

export class ArraySet implements BookSet {
  public index: number;
  constructor(public values: string[]) {
    this.index = -1;
  }
  public next(): string {
    this.index += 1;
    return this.values[this.index];
  }
  public skipTo(t: string) {
    let c,
      i = Math.max(0, this.index),
      v = this.values;
    while ((c = v[i]) && c < t) {
      i += 1;
    }
    this.index = i;
    return c;
  }
}

export default BookSet;
