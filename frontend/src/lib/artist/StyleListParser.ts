export class StyleListParser {
  static parse(value: string): string[] {
    const styles = value
      .split(",")
      .map((style) => style.trim())
      .filter((style) => style.length > 0);
    return [...new Set(styles)];
  }

  static format(styles: string[]): string {
    return styles.join(", ");
  }
}
