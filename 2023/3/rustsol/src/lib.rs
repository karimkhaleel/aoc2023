use std::fmt;
use std::u32;

use regex::Regex;

#[derive(Clone)]
struct TextObject<'a> {
    val: &'a str,
    start: usize,
    end: usize,
    is_part: bool,
}

impl fmt::Debug for TextObject<'_> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("TO")
            .field("val", &self.val)
            .field("part", &self.is_part)
            .finish()
    }
}

struct Line<'a> {
    numbers: Vec<TextObject<'a>>,
    symbols: Vec<TextObject<'a>>,
}

pub fn parse(lines: &Vec<&str>) -> u32 {
    let sym_re = Regex::new(r"([@$/\-\+#=*&])+").unwrap();
    let num_re = Regex::new(r"(\d+)+").unwrap();

    let mut nums = vec![];

    for i in 0..lines.len() {
        let last = if i > 0 {
            Some(Line {
                numbers: find_text_objects(lines[i - 1], &num_re),
                symbols: find_text_objects(lines[i - 1], &sym_re),
            })
        } else {
            None
        };
        let next = if i < lines.len() - 1 {
            Some(Line {
                numbers: find_text_objects(lines[i + 1], &num_re),
                symbols: find_text_objects(lines[i + 1], &sym_re),
            })
        } else {
            None
        };
        let mut current = Line {
            numbers: find_text_objects(lines[i], &num_re),
            symbols: find_text_objects(lines[i], &sym_re),
        };
        mark_adjacent(&mut current.numbers, &current.symbols);
        if let Some(mut next) = next {
            mark_adjacent(&mut next.numbers, &next.symbols);
            mark_adjacent(&mut next.numbers, &current.symbols);
            mark_adjacent(&mut current.numbers, &next.symbols);
        };
        if let Some(mut last) = last {
            mark_adjacent(&mut last.numbers, &current.symbols);
            println!("{:?}", last.numbers);
            last.numbers.iter().for_each(|n| {
                if n.is_part {
                    nums.push(n.val.parse().unwrap())
                }
            })
        }

        if i == lines.len() - 1 {
            current.numbers.iter().for_each(|n| {
                if n.is_part {
                    nums.push(n.val.parse().unwrap())
                }
            })
        }
    }

    nums.iter().for_each(|n| println!("{}", n));
    nums.iter().sum()
}

fn is_adjacent(start_a: usize, end_a: usize, start_b: usize, end_b: usize) -> bool {
    (end_a >= start_b && start_a <= start_b) || (start_a <= end_b && end_a >= end_b)
}

fn mark_adjacent(numbers: &mut Vec<TextObject>, symbols: &Vec<TextObject>) {
    numbers.iter_mut().for_each(|n| {
        symbols.iter().for_each(|s| {
            n.is_part = {
                let v = is_adjacent(n.start, n.end, s.start, s.end);
                if v {
                    println!("{}", n.val)
                }
                v
            }
        })
    });
}

fn find_text_objects<'a, 'b>(line: &'a str, re: &'b Regex) -> Vec<TextObject<'a>> {
    let mut part_numbers = vec![];
    for m in re.find_iter(line) {
        part_numbers.push(TextObject {
            val: m.as_str(),
            start: m.start(),
            end: m.end(),
            is_part: false,
        });
    }
    part_numbers
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mark_adjacent() {
        let sym_re = Regex::new(r"([@$/\-\+#=*&])+").unwrap();
        let num_re = Regex::new(r"(\d+)+").unwrap();

        let mut cases = vec![
            (
                find_text_objects("...123...", &num_re),
                find_text_objects("...123...", &sym_re),
                vec![false],
            ),
            (
                find_text_objects("...123*..", &num_re),
                find_text_objects("...123*..", &sym_re),
                vec![true],
            ),
            (
                find_text_objects("...123*..", &num_re),
                find_text_objects("..*123...", &sym_re),
                vec![true],
            ),
            (
                find_text_objects("...123..", &num_re),
                find_text_objects("......*.", &sym_re),
                vec![true],
            ),
            (
                find_text_objects("...123..", &num_re),
                find_text_objects(".....*..", &sym_re),
                vec![true],
            ),
            (
                find_text_objects("...123..", &num_re),
                find_text_objects("....*...", &sym_re),
                vec![true],
            ),
            (
                find_text_objects("...123..", &num_re),
                find_text_objects("...*....", &sym_re),
                vec![true],
            ),
            (
                find_text_objects("...123..", &num_re),
                find_text_objects("..*.....", &sym_re),
                vec![true],
            ),
            (
                find_text_objects("...***..", &num_re),
                find_text_objects("...123..", &sym_re),
                vec![],
            ),
            (
                find_text_objects("123...1.", &num_re),
                find_text_objects("...***..", &sym_re),
                vec![true, true],
            ),
            (
                find_text_objects("123...1.", &num_re),
                find_text_objects("...**...", &sym_re),
                vec![true, false],
            ),
            (
                find_text_objects("12....1.", &num_re),
                find_text_objects("...**...", &sym_re),
                vec![false, false],
            ),
            (
                find_text_objects("12....1.", &num_re),
                find_text_objects("...**...", &sym_re),
                vec![false, false],
            ),
            (
                find_text_objects("...1...", &num_re),
                find_text_objects("...*...", &sym_re),
                vec![true],
            ),
        ];

        cases.iter_mut().enumerate().for_each(|(index, case)| {
            mark_adjacent(&mut case.0, &case.1);
            let parts: Vec<bool> = case.0.iter().map(|textobj| textobj.is_part).collect();
            assert_eq!(case.2, parts, "Case: {}", index);
        })
    }

    #[test]
    fn test_full() {
        let cases = vec![
            (vec!["1", "*"], 1),
            (vec!["*", "1"], 1),
            (vec!["1", "1"], 0),
            (vec!["*", "*"], 0),
            (vec!["*", "*", "1"], 1),
            (vec!["1", "1", "*"], 1),
            (vec!["1", "1", "*", "*"], 1),
            (vec!["1", "1", "*", "1"], 2),
            (vec!["1.1", ".*."], 2),
            (vec!["*.*", ".1."], 1),
            (vec!["1...1", "..*.."], 0),
            (vec!["1...1", ".**.."], 1),
            (vec!["1....", ".*...", "1...."], 2),
            (vec!["1.1", ".*.", "1.1"], 4),
            (vec!["1.1", ".*.", "..."], 2),
            (vec!["1.1", "...", "1.1"], 0),
            (vec![".*.", ".*.", "111"], 111),
        ];

        cases.iter().enumerate().for_each(|(index, case)| {
            assert_eq!(parse(&case.0), case.1, "{}", index);
        })
    }
    #[test]
    fn test_example() {
        let cases = vec![(
            vec![
                "467..114..",
                "...*......",
                "..35..633.",
                "......#...",
                "617*......",
                ".....+.57.",
                "..592.....",
                "......755.",
                "...$.*....",
                ".664.597..",
            ],
            4361,
        )];

        cases.iter().enumerate().for_each(|(index, case)| {
            assert_eq!(parse(&case.0), case.1, "{}", index);
        })
    }
}
