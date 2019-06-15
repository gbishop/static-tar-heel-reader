/* Experiment with a class to represent sets of books */

export interface BookSet {
  current: string;
  next: () => string;
  skipTo: (value: string) => string;
  backTo: (value: string) => string;
}

export class Intersection implements BookSet {
  constructor(public A: BookSet, public B: BookSet) {}
  public current: string;
  align(a: string, b: string): string {
    while (a && b && a != b) {
      if (a < b) {
        a = this.A.skipTo(b);
      } else {
        b = this.B.skipTo(a);
      }
    }
    this.current = (a && b) || '';
    return this.current;
  }
  public next(): string {
    let a = this.A.next();
    let b = this.B.next();
    return this.align(a, b);
  }
  public skipTo(v: string): string {
    let a = this.A.skipTo(v);
    let b = this.B.skipTo(v);
    return this.align(a, b);
  }
  public backTo(v: string): string {
    let a = this.A.backTo(v);
    let b = this.B.backTo(v);
    return this.align(a, b);
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
  public current: string;
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
    this.current = v;
    if (v > this.stop || v < this.start) {
      return '';
    }
    return v;
  }
  public backTo(v: string) {
    this.current = v;
    if (this.current < this.start) {
      this.current = this.start;
    }
    return this.current;
  }
}

export class ArraySet implements BookSet {
  public index = -1;
  public current: string;
  constructor(public values: string[]) {}
  public next(): string {
    this.index += 1;
    if (this.index < this.values.length) {
      this.current = this.values[this.index];
      return this.current;
    } else {
      return '';
    }
  }
  public skipTo(v: string) {
    while (this.index < this.values.length && this.values[this.index] < v) {
      this.index += 1;
    }
    if (this.index < this.values.length) {
      this.current = this.values[this.index];
      return this.current;
    } else {
      return '';
    }
  }
  public backTo(v: string) {
    this.index = this.values.lastIndexOf(v, this.index);
    if (this.index > -1) {
      this.current = this.values[this.index];
      return this.current;
    }
    return '';
  }
}

export class StringSet implements BookSet {
  public index = -1;
  public current: string = '';
  constructor(public values: string) {}
  public next(): string {
    this.index += 1;
    const i = this.index * 3;
    if (this.index < this.values.length) {
      this.current = this.values.slice(i, i + 3);
      return this.current;
    } else {
      return '';
    }
  }
  public skipTo(v: string) {
    let c;
    if (v >= this.current) {
      for (let i = this.index * 3; i < this.values.length; i += 3) {
        c = this.values.slice(i, i + 3);
        if (c >= v) {
          this.index = i / 3;
          this.current = c;
          return this.current;
        }
      }
    } else {
      for (let i = this.index * 3; i >= 0; i -= 3) {
        c = this.values.slice(i, i + 3);
        if (c <= v) {
          this.index = i / 3;
          this.current = c;
          return this.current;
        }
      }
    }
    return '';
  }
  public backTo(v: string) {
    let c;
    for (let i = this.index * 3; i < this.values.length; i -= 3) {
      c = this.values.slice(i, i + 3);
      if (c >= v) {
        this.index = i / 3;
        this.current = c;
        return this.current;
      }
    }
    return '';
  }
}

export default ArraySet;