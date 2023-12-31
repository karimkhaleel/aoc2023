use core::panic;
use std::{cmp::Ordering, collections::HashMap, fs};

#[derive(Debug)]
struct Hand<'a> {
    hand: Vec<u32>,
    cards: &'a str,
    points: u32,
    rank: u8,
}

impl<'a> Hand<'a> {
    fn new(line: &'a str) -> Result<Self, &'static str> {
        let mut parts = line.split_whitespace();
        let cards = match parts.next() {
            Some(n) => n,
            None => return Err("Failed"),
        };
        let points: u32 = parts.next().unwrap().parse().unwrap();
        let numerical_cards: Vec<u32> = cards
            .chars()
            .map(|c| match c.to_digit(10) {
                Some(n) => n,
                None => match c {
                    'A' => 14,
                    'K' => 13,
                    'Q' => 12,
                    'J' => 11,
                    'T' => 10,
                    _ => panic!(),
                },
            })
            .collect();

        let frequencies = numerical_cards.iter().fold(HashMap::new(), |mut acc, &n| {
            *acc.entry(n).or_insert(0) += 1;
            acc
        });

        let mut values: Vec<_> = frequencies.values().cloned().collect();

        values.sort_unstable();

        let rank = match values.as_slice() {
            [1, 1, 1, 2] => 1,
            [1, 2, 2] => 2,
            [1, 1, 3] => 3,
            [2, 3] => 4,
            [1, 4] => 5,
            [5] => 6,
            _ => 0,
        };

        Ok(Hand {
            hand: numerical_cards,
            cards,
            points,
            rank,
        })
    }

    fn new2(line: &'a str) -> Result<Self, &'static str> {
        let mut parts = line.split_whitespace();
        let cards = match parts.next() {
            Some(n) => n,
            None => return Err("Failed"),
        };
        let points: u32 = parts.next().unwrap().parse().unwrap();
        let numerical_cards: Vec<u32> = cards
            .chars()
            .map(|c| match c.to_digit(10) {
                Some(n) => n,
                None => match c {
                    'A' => 14,
                    'K' => 13,
                    'Q' => 12,
                    'J' => 1,
                    'T' => 10,
                    _ => panic!(),
                },
            })
            .collect();

        let mut frequencies = numerical_cards.iter().fold(HashMap::new(), |mut acc, &n| {
            *acc.entry(n).or_insert(0) += 1;
            acc
        });

        let rank = if let Some(v) = frequencies.remove(&1) {
            let _ = frequencies.insert(1, 0);
            let mut values: Vec<_> = frequencies.values().cloned().collect();
            values.sort_unstable();
            let len = values.len();
            values[len - 1] += v;

            match values.as_slice() {
                [0, 1, 1, 1, 2] => 1,
                [0, 2, 2] => 2,
                [0, 1, 1, 3] => 3,
                [0, 2, 3] => 4,
                [0, 1, 4] => 5,
                [0, 5] | [5] => 6,
                _ => 0,
            }
        } else {
            let mut values: Vec<_> = frequencies.values().cloned().collect();

            values.sort_unstable();

            match values.as_slice() {
                [1, 1, 1, 2] => 1,
                [1, 2, 2] => 2,
                [1, 1, 3] => 3,
                [2, 3] => 4,
                [1, 4] => 5,
                [5] => 6,
                _ => 0,
            }
        };

        Ok(Hand {
            hand: numerical_cards,
            cards,
            points,
            rank,
        })
    }
}

impl PartialEq for Hand<'_> {
    fn eq(&self, other: &Self) -> bool {
        if self.rank != other.rank {
            return false;
        }

        if self.hand != other.hand {
            return false;
        }

        true
    }
}

impl PartialOrd for Hand<'_> {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        let diff_rank = self.rank as i16 - other.rank as i16;
        if diff_rank < 0 {
            return Some(Ordering::Less);
        } else if diff_rank > 0 {
            return Some(Ordering::Greater);
        }

        for (&c1, &c2) in self.hand.iter().zip(other.hand.iter()) {
            match c1.cmp(&c2) {
                Ordering::Less => return Some(Ordering::Less),
                Ordering::Greater => return Some(Ordering::Greater),
                _ => continue,
            };
        }

        Some(Ordering::Equal)
    }
}

impl Eq for Hand<'_> {}

impl Ord for Hand<'_> {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

fn main() {
    let content = fs::read_to_string("../input.txt").unwrap();
    let lines = content.split("\n");
    let mut hands: Vec<_> = lines.filter_map(|l| Hand::new2(l).ok()).collect();
    hands.sort_unstable();

    let _ = fs::write(
        "../test2output.txt",
        hands.iter().fold(String::new(), |mut acc, h| {
            acc.push_str(&format!("{} {}\n", h.cards, h.points));
            acc
        }),
    );

    let result = hands.iter().enumerate().fold(0, |mut acc, (i, h)| {
        acc += h.points * (i as u32 + 1);
        acc
    });

    println!("{result:?}");
}
